#!/usr/bin/env python3
"""
Proof Audit Verifier
Retrieves the full audit trail and verifies each entry’s hash.

Usage:
    python verify.py
    python verify.py --type milestone
    python verify.py --agent hetzy_phd

UrantiOS: Truth · Beauty · Goodness
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from proof_logger.logger import get_audit_trail, verify_hash


def main():
    parser = argparse.ArgumentParser(description="Verify proof audit trail")
    parser.add_argument("--type",  help="milestone | agent_action")
    parser.add_argument("--agent", help="filter by agent_id")
    args = parser.parse_args()

    records = get_audit_trail(filter_type=args.type, agent_id=args.agent)

    print("=" * 64)
    print("PROOF AUDIT TRAIL — INTEGRITY VERIFICATION")
    print("UrantiOS: Truth · Beauty · Goodness")
    print("=" * 64)
    print(f"Records: {len(records)}")

    passed = failed = 0
    for i, rec in enumerate(records, 1):
        meta   = rec.get("metadata", {})
        rtype  = meta.get("type", "?")
        rid    = meta.get("milestone_id") or meta.get("agent_id", "?")
        ts     = meta.get("timestamp", "?")
        ok     = verify_hash(dict(meta))
        status = "✓ VERIFIED" if ok else "✗ TAMPERED"
        (passed if ok else failed).__class__  # side-effect-free; increment below
        if ok: passed += 1
        else:  failed += 1

        print(f"\n[{i}] {status}  {rtype} | {rid} | {ts[:19]}")
        if not ok:
            print("     ⚠ ALERT: hash mismatch — record may have been altered!")
        print(f"     {rec['memory'][:120]}")

    print()
    print(f"Result: {passed} verified | {failed} failed")
    if failed:
        print("⚠ ALERT: Tampered records detected. Investigate immediately.")
    else:
        print("All records pass integrity check.")
    print("=" * 64)


if __name__ == "__main__":
    main()
