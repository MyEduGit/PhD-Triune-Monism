"""
Proof Logger — AI Legislature Phase 5: Milestone Verification

Logs PhD milestones and agent actions to Mem0 with SHA-256 hashing
for tamper detection and immutable audit trail.

UrantiOS: Truth · Beauty · Goodness
"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from mem0_pilot.config import MEM0_CONFIG, USER_ID

PROOF_AGENT_ID  = "proof_logger_v1"
PROOF_COLLECTION = "proof_log"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _hash(data: dict) -> str:
    canonical = json.dumps(data, sort_keys=True, ensure_ascii=True)
    return hashlib.sha256(canonical.encode()).hexdigest()


def _get_memory():
    from mem0 import Memory
    cfg = json.loads(json.dumps(MEM0_CONFIG))
    cfg["vector_store"]["config"]["collection_name"] = PROOF_COLLECTION
    return Memory.from_config(cfg)


def log_milestone(
    milestone_id: str,
    title: str,
    description: str,
    evidence: list[str],
    phd_phase: str = "",
    legislature_phase: str = "",
    agent_id: str = "mircea",
) -> dict:
    """Log a verified milestone. Returns the proof record including its hash."""
    m = _get_memory()
    record = {
        "type":              "milestone",
        "milestone_id":      milestone_id,
        "title":             title,
        "description":       description,
        "evidence":          evidence,
        "phd_phase":         phd_phase,
        "legislature_phase": legislature_phase,
        "logged_by":         agent_id,
        "timestamp":         _now(),
    }
    record["hash"] = _hash({k: v for k, v in record.items() if k != "hash"})

    text = (
        f"MILESTONE PROOF: {milestone_id} — {title}. "
        f"{description} "
        f"Evidence: {'; '.join(evidence)}. "
        f"PhD Phase: {phd_phase}. Legislature Phase: {legislature_phase}. "
        f"Agent: {agent_id}. Hash: {record['hash']}."
    )
    m.add(
        [{"role": "user", "content": text}],
        user_id=USER_ID,
        agent_id=PROOF_AGENT_ID,
        metadata={**record, "evidence": json.dumps(evidence)},
    )
    print(f"[proof] milestone: {milestone_id} | hash={record['hash'][:16]}…")
    return record


def log_agent_action(
    agent_id: str,
    action: str,
    result: str,
    passed_lucifer_test: bool,
    mandate: str = "",
) -> dict:
    """Log an agent action with Lucifer Test result. Failed tests are flagged permanently."""
    m = _get_memory()
    record = {
        "type":               "agent_action",
        "agent_id":           agent_id,
        "action":             action,
        "result":             result,
        "passed_lucifer_test": passed_lucifer_test,
        "mandate":            mandate,
        "timestamp":          _now(),
    }
    record["hash"] = _hash({k: v for k, v in record.items() if k != "hash"})

    flag = "PASS" if passed_lucifer_test else "FAIL — FLAGGED"
    text = (
        f"AGENT ACTION: {agent_id} executed '{action}'. "
        f"Result: {result}. "
        f"Lucifer Test: {flag}. "
        f"Mandate: {mandate}. "
        f"Hash: {record['hash']}."
    )
    m.add(
        [{"role": "user", "content": text}],
        user_id=USER_ID,
        agent_id=PROOF_AGENT_ID,
        metadata=record,
    )
    icon = "✓" if passed_lucifer_test else "✗ LUCIFER FAIL"
    print(f"[proof] action: {agent_id} | {icon} | hash={record['hash'][:16]}…")
    return record


def get_audit_trail(filter_type: str = None, agent_id: str = None) -> list:
    """Retrieve all proof records, optionally filtered by type or agent."""
    m = _get_memory()
    all_mem = m.get_all(user_id=USER_ID) or []
    results = []
    for mem in all_mem:
        meta = mem.get("metadata", {})
        if filter_type and meta.get("type") != filter_type:
            continue
        if agent_id and meta.get("agent_id") != agent_id:
            continue
        results.append({"memory": mem.get("memory", ""), "metadata": meta})
    return results


def verify_hash(record: dict) -> bool:
    """Verify a record’s hash for tamper detection."""
    stored = record.get("hash")
    check  = _hash({k: v for k, v in record.items() if k != "hash"})
    return stored == check
