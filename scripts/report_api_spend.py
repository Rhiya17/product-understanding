"""Reconcile local API records without treating reservations as billed usage.

Read-only: no provider calls, queue changes, or billing mutations. Includes all
locally recorded project history and a separate America/Los_Angeles day subtotal.
Provider invoices remain authoritative; external agent/tool usage may be absent.
"""
import argparse
from collections import defaultdict
from datetime import datetime
import json
from pathlib import Path
import sqlite3
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
TZ = ZoneInfo('America/Los_Angeles')


def provider_for(label):
    label = label.lower()
    if label.startswith('openai/'):
        return 'OpenAI'
    if label.startswith('anthropic/'):
        return 'Anthropic'
    if 'fal' in label or label.startswith('bytedance/'):
        return 'fal.ai'
    return 'Unclassified'


def reconcile(video_rows, events, manifests):
    settlements = {e['reservation_id']: e for e in events
                   if e.get('event') == 'settle' and e.get('reservation_id')}
    rows = {}
    for r in video_rows:
        rows[r['id']] = dict(id=r['id'], at=r['at'], provider=provider_for(r['label']),
                             label=r['label'], job_id=r['job_id'],
                             category='video_generation', reserved_or_recorded_usd=r['amount'])
    for index, e in enumerate(events):
        if e.get('event') != 'reserve':
            continue
        rid = e.get('reservation_id')
        if e.get('category') == 'video_generation' and not rid:
            # Older video reservations lacked IDs in JSONL. SQLite is their
            # authoritative identity; never add the same video call twice.
            matches = [r for r in rows.values() if r.get('job_id') == e.get('job_id')
                       and r['label'] == e.get('label') and r['at'] == e.get('at')]
            if matches:
                continue
        rid = rid or f'unidentified-ledger-reservation-{index}'
        if rid in rows:
            continue
        manifest = manifests.get(e.get('run_id'), {})
        rows[rid] = dict(id=rid, at=e.get('at'),
                         provider=provider_for(manifest.get('provider', '') or e.get('label', '')),
                         label=e.get('label'), run_id=e.get('run_id'), job_id=e.get('job_id'),
                         category=e.get('category'), model=manifest.get('model'),
                         reserved_or_recorded_usd=e.get('worst_case_usd', 0))
    for rid, row in rows.items():
        settlement = settlements.get(rid)
        value = settlement.get('actual_usd') if settlement else None
        row['status'] = 'settled_estimate' if value is not None else 'unreconciled'
        row['settled_estimated_usd'] = value
        row['unreconciled_reservation_usd'] = row['reserved_or_recorded_usd'] if value is None else 0
        row['outcome'] = settlement.get('outcome') if settlement else None
    return list(rows.values())


def summarize(rows):
    providers = defaultdict(lambda: dict(settled_estimated_usd=0, unreconciled_reservation_usd=0,
                                         settled_calls=0, unreconciled_calls=0))
    for row in rows:
        p = providers[row['provider']]
        p['settled_estimated_usd'] += row['settled_estimated_usd'] or 0
        p['unreconciled_reservation_usd'] += row['unreconciled_reservation_usd']
        p['settled_calls' if row['status'] == 'settled_estimate' else 'unreconciled_calls'] += 1
    for p in providers.values():
        for key in ('settled_estimated_usd', 'unreconciled_reservation_usd'):
            p[key] = round(p[key], 6)
    return dict(providers=providers,
                settled_estimated_usd=round(sum(p['settled_estimated_usd'] for p in providers.values()), 6),
                unreconciled_reservation_usd=round(sum(p['unreconciled_reservation_usd'] for p in providers.values()), 6))


def report(day=None):
    today = day or datetime.now(TZ).date().isoformat()
    ledger = ROOT / 'docs/workorders/approvals/spend-ledger.jsonl'
    events = [json.loads(line) for line in ledger.read_text().splitlines() if line.strip()]
    manifests = {}
    for path in (ledger.parent / 'manifests').glob('*.json'):
        item = json.loads(path.read_text())
        manifests[item.get('run_id')] = item
    with sqlite3.connect(f'file:{ROOT / "var/showme/showme.db"}?mode=ro', uri=True) as db:
        db.row_factory = sqlite3.Row
        videos = [dict(row) for row in db.execute('SELECT * FROM spend')]
    rows = reconcile(videos, events, manifests)
    day_rows = [r for r in rows if r['at'] and datetime.fromisoformat(r['at']).astimezone(TZ).date().isoformat() == today]
    payments = ROOT / 'output/api-costs/user-reported-topups.json'
    return dict(generated_at=datetime.now(TZ).isoformat(), currency='USD', timezone=str(TZ),
                accounting_basis='Local recorded cost estimates; not provider invoices.',
                project_all_time=summarize(rows), selected_day=today, day=summarize(day_rows),
                user_reported_topups=json.loads(payments.read_text()) if payments.exists() else [],
                limitations=[
                    'Top-ups are deposits, not usage spending; they are excluded from usage totals.',
                    'Unreconciled reservations include active, failed, or unknown-outcome calls; they are not confirmed charges.',
                    'Recorded estimates use each pipeline\'s pricing calculation and may differ from invoices.',
                    'External Claude agent extraction, image generation tools, and any unlogged provider calls require separate billing/usage records.',
                    'ChatGPT/Codex/Claude subscription fees and account balances are not inferred from this ledger.'
                ], calls=rows)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--day', help='Local date YYYY-MM-DD; defaults to today')
    args = parser.parse_args()
    print(json.dumps(report(args.day), indent=2))
