"""Paid-run authorization and spend ledger.

Authorized spend is $0 until the owner approves an exact run manifest. A
manifest is frozen by its SHA-256 digest; the owner's approval is a separate
append-only receipt bound to that digest. Every billable call reserves its
worst-case cost first, and the smallest remaining limit wins: the approved
run cap, the category ceiling, and the cumulative ceiling across categories.

Credentials, configured budgets and work-order ceilings never start a run.
An approval authorizes one run. A changed manifest, a rerun, or unknown spend
needs a fresh owner decision.
"""

import hashlib
import json
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_APPROVALS = REPO_ROOT / "docs" / "workorders" / "approvals" / "paid-runs.jsonl"
DEFAULT_LEDGER = REPO_ROOT / "docs" / "workorders" / "approvals" / "spend-ledger.jsonl"

# Maximum approval requests from the work order, not standing authorization.
CATEGORY_CEILINGS_USD = {
    "answer_verifier": 5.0,
    "astra_authoring": 30.0,
    "onboarding": 10.0,
    "video_generation": 100.0,  # Owner approved $100 total in chat on 2026-10-07.
}
PER_RUN_CEILINGS_USD = {"astra_authoring": 15.0}
TOTAL_CEILING_USD = 45.0
REQUIRED_MANIFEST_FIELDS = (
    "run_id", "category", "purpose", "provider", "model", "inputs",
    "max_calls", "cap_usd", "retry_policy",
)


class SpendRefused(Exception):
    """A paid operation was not authorized or would exceed a limit."""


def manifest_digest(manifest):
    canonical = json.dumps(manifest, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _now():
    return datetime.now(timezone.utc)


def _read_jsonl(path):
    path = Path(path)
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines()
            if line.strip()]


def _append_jsonl(path, entry):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as handle:
        handle.write(json.dumps(entry, sort_keys=True) + "\n")


def validate_manifest(manifest):
    missing = [f for f in REQUIRED_MANIFEST_FIELDS if f not in manifest]
    if missing:
        raise SpendRefused(f"manifest missing fields: {', '.join(missing)}")
    category = manifest["category"]
    if category not in CATEGORY_CEILINGS_USD:
        raise SpendRefused(f"unknown paid-run category: {category}")
    cap = float(manifest["cap_usd"])
    ceiling = PER_RUN_CEILINGS_USD.get(category, CATEGORY_CEILINGS_USD[category])
    if not 0 < cap <= ceiling:
        raise SpendRefused(
            f"run cap ${cap:.2f} outside (0, ${ceiling:.2f}] for {category}")


def record_owner_approval(manifest, approved_by, approvals_path=DEFAULT_APPROVALS,
                          expires_at=None, note=""):
    """Append the owner's approval receipt for this exact manifest.

    Call only from an owner-facing command after the owner has explicitly
    approved this manifest. Never call it from agent or request-serving code.
    """
    validate_manifest(manifest)
    receipt = {
        "event": "approved",
        "approval_id": "appr_" + uuid.uuid4().hex[:12],
        "manifest_digest": manifest_digest(manifest),
        "run_id": manifest["run_id"],
        "category": manifest["category"],
        "approved_cap_usd": float(manifest["cap_usd"]),
        "approved_by": approved_by,
        "approved_at": _now().isoformat(timespec="seconds"),
        "expires_at": expires_at,
        "note": note,
    }
    _append_jsonl(approvals_path, receipt)
    return receipt


def revoke_approval(approval_id, revoked_by, approvals_path=DEFAULT_APPROVALS):
    _append_jsonl(approvals_path, {
        "event": "revoked", "approval_id": approval_id,
        "revoked_by": revoked_by,
        "revoked_at": _now().isoformat(timespec="seconds"),
    })


@dataclass
class _Totals:
    run: float
    category: float
    total: float


class SpendGuard:
    def __init__(self, approvals_path=DEFAULT_APPROVALS, ledger_path=DEFAULT_LEDGER):
        self.approvals_path = Path(approvals_path)
        self.ledger_path = Path(ledger_path)

    def _receipt(self, approval_id):
        receipt, revoked = None, False
        for entry in _read_jsonl(self.approvals_path):
            if entry.get("approval_id") != approval_id:
                continue
            if entry["event"] == "approved":
                receipt = entry
            elif entry["event"] == "revoked":
                revoked = True
        if receipt is None:
            raise SpendRefused(f"no owner approval recorded for {approval_id!r}")
        if revoked:
            raise SpendRefused(f"approval {approval_id} was revoked")
        expires = receipt.get("expires_at")
        if expires and datetime.fromisoformat(expires) <= _now():
            raise SpendRefused(f"approval {approval_id} expired")
        return receipt

    def _committed(self, category, approval_id):
        """Spend counted against limits: settled actuals plus open or unknown
        reservations at their reserved worst case."""
        reservations = {}
        for index, entry in enumerate(_read_jsonl(self.ledger_path)):
            if entry["event"] == "reserve":
                # Older app-side video reservations carry no reservation_id;
                # they can never be paired with a settlement, so they stay
                # counted at their worst case (conservative).
                key = entry.get("reservation_id") or f"unpaired:{index}"
                reservations[key] = dict(entry)
            elif entry["event"] == "settle":
                row = reservations.get(entry.get("reservation_id"))
                if row is None:
                    continue
                if entry.get("actual_usd") is not None:
                    row["counted"] = float(entry["actual_usd"])
                row["settled"] = True
        totals = _Totals(0.0, 0.0, 0.0)
        for row in reservations.values():
            amount = row.get("counted", float(row["worst_case_usd"]))
            totals.total += amount
            if row["category"] == category:
                totals.category += amount
            if row["approval_id"] == approval_id:
                totals.run += amount
        return totals

    def _run_events(self, approval_id):
        return [e for e in _read_jsonl(self.ledger_path)
                if e.get("approval_id") == approval_id]

    def authorize(self, manifest, approval_id):
        """Return a run authorization, or raise SpendRefused."""
        validate_manifest(manifest)
        receipt = self._receipt(approval_id)
        if receipt["manifest_digest"] != manifest_digest(manifest):
            raise SpendRefused(
                "manifest differs from the approved digest; changed inputs, "
                "provider, model or attempt plan need a fresh approval")
        events = self._run_events(approval_id)
        if any(e["event"] == "finish" for e in events):
            raise SpendRefused(
                f"approval {approval_id} was already used; a rerun needs a "
                "fresh approval")
        if any(e["event"] == "settle" and e.get("actual_usd") is None
               for e in events):
            raise SpendRefused(
                "a previous submission has unknown billing; reconcile it "
                "before any further paid call")
        return RunAuthorization(self, manifest, receipt)


class RunAuthorization:
    def __init__(self, guard, manifest, receipt):
        self.guard = guard
        self.manifest = manifest
        self.receipt = receipt
        self.category = manifest["category"]
        self.approval_id = receipt["approval_id"]
        self.cap = min(float(receipt["approved_cap_usd"]),
                       float(manifest["cap_usd"]))
        self.calls = sum(1 for e in guard._run_events(self.approval_id)
                         if e["event"] == "reserve")
        self.stopped_reason = None

    def remaining_usd(self):
        totals = self.guard._committed(self.category, self.approval_id)
        return min(self.cap - totals.run,
                   CATEGORY_CEILINGS_USD[self.category] - totals.category,
                   TOTAL_CEILING_USD - totals.total)

    def reserve(self, worst_case_usd, label):
        """Reserve the worst-case cost of the next billable call."""
        if self.stopped_reason:
            raise SpendRefused(f"run stopped: {self.stopped_reason}")
        if self.calls >= int(self.manifest["max_calls"]):
            raise SpendRefused("approved call limit reached")
        worst = float(worst_case_usd)
        if worst <= 0:
            raise SpendRefused("worst-case cost must be a positive bound")
        remaining = self.remaining_usd()
        if worst > remaining + 1e-9:
            raise SpendRefused(
                f"call {label!r} worst case ${worst:.4f} exceeds remaining "
                f"${remaining:.4f}")
        reservation_id = "res_" + uuid.uuid4().hex[:12]
        _append_jsonl(self.guard.ledger_path, {
            "event": "reserve", "reservation_id": reservation_id,
            "approval_id": self.approval_id, "run_id": self.manifest["run_id"],
            "category": self.category, "label": label,
            "worst_case_usd": worst, "at": _now().isoformat(timespec="seconds"),
        })
        self.calls += 1
        return reservation_id

    def settle(self, reservation_id, actual_usd, outcome, provider_call_id=None):
        """Record the call outcome. actual_usd=None means billing is unknown:
        the full reservation stays counted and further paid work stops."""
        _append_jsonl(self.guard.ledger_path, {
            "event": "settle", "reservation_id": reservation_id,
            "approval_id": self.approval_id,
            "actual_usd": None if actual_usd is None else float(actual_usd),
            "outcome": outcome, "provider_call_id": provider_call_id,
            "at": _now().isoformat(timespec="seconds"),
        })
        if actual_usd is None:
            self.stopped_reason = "unknown billing on " + reservation_id

    def finish(self, outcome):
        _append_jsonl(self.guard.ledger_path, {
            "event": "finish", "approval_id": self.approval_id,
            "run_id": self.manifest["run_id"], "outcome": outcome,
            "remaining_unspent_usd": round(max(self.remaining_usd(), 0), 4),
            "at": _now().isoformat(timespec="seconds"),
        })
