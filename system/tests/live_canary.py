#!/usr/bin/env python3
"""Small live Qwen canary. CI runs this only when FAL_KEY is configured."""

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from system import verify_claims as verifier


REPO_ROOT = Path(__file__).resolve().parents[2]

# These exact repository claims cover the three v1 false-alarm classes and
# the three genuine defects found in the owner's spot-check.
CASES = [
    ("graco-ready2jet-2212125", "claim_r2j_step_fold_1", "ENTAILED"),
    ("graco-snugride-35-lite-lx", "claim_srl_spec_dimensions", "ENTAILED"),
    ("levoit-core-300s", "claim_c300s_spec_standby_power", "ENTAILED"),
    ("apple-macbook-air-13-m3", "claim_mba_spec_wifi_standard", "ENTAILED"),
    ("levoit-core-300s", "claim_c300s_limit_room_size", "MEANING_CHANGED"),
    ("bose-qc-ultra-headphones", "claim_bqcu2_bluetooth_range_1",
     "MEANING_CHANGED"),
    ("bose-qc-ultra-headphones", "claim_bqcu2_compat_bose_speakers_1",
     "MEANING_CHANGED"),
]


def load_claim(product, claim_id):
    path = REPO_ROOT / "evidence-packs" / product / "claims.json"
    claims = json.loads(path.read_text(encoding="utf-8"))
    return next(claim for claim in claims if claim["claim_id"] == claim_id)


def main():
    if not os.environ.get("FAL_KEY"):
        print("live canary skipped: FAL_KEY is not configured")
        return 0
    failures = 0
    for index, (product, claim_id, expected) in enumerate(CASES, 1):
        claim = load_claim(product, claim_id)
        result, serving_model, _cost, malformed, _calls = \
            verifier._invoke_for_verdict(
                verifier.build_prompt(claim), verifier.call_provider)
        print(f"canary {index} {claim_id}: {result['verdict']} "
              f"(expected {expected}) via {serving_model}")
        if (malformed or result["verdict"] != expected
                or serving_model != verifier.MODEL_ID):
            failures += 1
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
