#!/usr/bin/env python3
"""Small live Qwen canary. CI runs this only when FAL_KEY is configured."""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from system import verify_claims as verifier


CASES = [
    ({"value": 30, "unit": "lb"}, "ENTAILED"),
    ({"value": 35, "unit": "lb"}, "MEANING_CHANGED"),
    ({"value": 30, "unit": "kg"}, "MEANING_CHANGED"),
]


def main():
    if not os.environ.get("FAL_KEY"):
        print("live canary skipped: FAL_KEY is not configured")
        return 0
    failures = 0
    for index, (value, expected) in enumerate(CASES, 1):
        claim = {
            "type": "LIMIT",
            "predicate": "maximum_weight",
            "object": value,
            "consequence_ceiling": "C3",
            "source_bindings": [{
                "source_id": "canary",
                "page": None,
                "quote": "The maximum supported weight is 30 lb.",
            }],
        }
        result, malformed, _calls = verifier._invoke_for_verdict(
            verifier.build_prompt(claim, 0), verifier.call_provider)
        print(f"canary {index}: {result['verdict']}")
        if malformed or result["verdict"] != expected:
            failures += 1
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
