#!/usr/bin/env python3
"""
Obsidian Bridge — Vault Ingestion
Parses Obsidian markdown files (PhD diary, TOE_DIARY, research notes)
and ingests each section as a Mem0 memory with structured metadata.

Usage:
    python ingest_vault.py                             # uses OBSIDIAN_VAULT_PATH from .env
    python ingest_vault.py /path/to/obsidian/vault
    python ingest_vault.py --dry-run                   # count chunks without storing

UrantiOS: Truth · Beauty · Goodness
"""
import os
import sys
import time
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from mem0_pilot.config import MEM0_CONFIG, USER_ID

VAULT_AGENT_ID   = "obsidian_bridge_v1"
VAULT_COLLECTION = "obsidian_vault"
CHUNK_MIN_CHARS  = 150

# Files to ingest first (most PhD-relevant)
PRIORITY = [
    "PhD-Research-Diary", "TOE_DIARY", "PhD-Proposal",
    "PhD-Track-Decision", "Research-Methods",
]


def get_vault_path(override: str = None) -> Path:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent.parent / ".env")
    raw = override or os.getenv("OBSIDIAN_VAULT_PATH") or str(Path.home() / "Documents" / "Obsidian")
    p = Path(raw)
    if not p.exists():
        raise FileNotFoundError(
            f"Vault not found: {p}\n"
            "Set OBSIDIAN_VAULT_PATH in .env or pass path as argument."
        )
    return p


def _get_memory():
    import json
    from mem0 import Memory
    cfg = json.loads(__import__("json").dumps(MEM0_CONFIG))
    cfg["vector_store"]["config"]["collection_name"] = VAULT_COLLECTION
    return Memory.from_config(cfg)


def parse_frontmatter(text: str) -> tuple[dict, str]:
    meta = {}
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            for line in text[3:end].strip().splitlines():
                if ":" in line:
                    k, _, v = line.partition(":")
                    meta[k.strip()] = v.strip()
            text = text[end+3:].strip()
    return meta, text


def chunk_by_heading(content: str, filename: str) -> list[dict]:
    """Split on ## headings, return list of {heading, text}."""
    chunks, heading, lines = [], filename, []
    for line in content.splitlines():
        if line.startswith("# ") or line.startswith("## "):
            if lines:
                text = "\n".join(lines).strip()
                if len(text) >= CHUNK_MIN_CHARS:
                    chunks.append({"heading": heading, "text": text})
            heading = line.lstrip("#").strip()
            lines = []
        else:
            lines.append(line)
    if lines:
        text = "\n".join(lines).strip()
        if len(text) >= CHUNK_MIN_CHARS:
            chunks.append({"heading": heading, "text": text})
    return chunks


def ingest_file(m, filepath: Path, vault_root: Path, dry_run: bool) -> int:
    relative = str(filepath.relative_to(vault_root))
    content  = filepath.read_text(encoding="utf-8", errors="ignore")
    frontmatter, body = parse_frontmatter(content)
    chunks = chunk_by_heading(body, filepath.stem)
    added = 0
    for chunk in chunks:
        text = (
            f"[Obsidian: {relative}] "
            f"Section: {chunk['heading']}. "
            f"{chunk['text'][:1500]}"
        )
        meta = {
            "source":     "obsidian",
            "file":       relative,
            "heading":    chunk["heading"],
            **{k: v for k, v in frontmatter.items() if isinstance(v, str)},
        }
        if not dry_run:
            try:
                m.add(
                    [{"role": "user", "content": text}],
                    user_id=USER_ID,
                    agent_id=VAULT_AGENT_ID,
                    metadata=meta,
                )
                added += 1
            except Exception as exc:
                print(f"  [warn] {filepath.name} / {chunk['heading']}: {exc}")
        else:
            added += 1
    return added


def main():
    parser = argparse.ArgumentParser(description="Ingest Obsidian vault into Mem0")
    parser.add_argument("vault", nargs="?", help="path to vault (overrides .env)")
    parser.add_argument("--dry-run", action="store_true", help="count chunks only")
    args = parser.parse_args()

    vault = get_vault_path(args.vault)
    print("=" * 60)
    print("OBSIDIAN BRIDGE — Vault Ingestion")
    print(f"Vault  : {vault}")
    print(f"Dry run: {args.dry_run}")
    print("UrantiOS: Truth · Beauty · Goodness")
    print("=" * 60)

    m = _get_memory() if not args.dry_run else None

    # Sort: priority files first
    all_md = list(vault.rglob("*.md"))
    all_md.sort(key=lambda p: (not any(pat in p.name for pat in PRIORITY), p.name))

    total_files = total_chunks = 0
    t0 = time.time()
    for md in all_md:
        if any(skip in str(md) for skip in (".git", ".trash", ".obsidian")):
            continue
        n = ingest_file(m, md, vault, args.dry_run)
        if n:
            print(f"  {'(dry) ' if args.dry_run else ''}+ {md.name}: {n} chunks")
            total_files  += 1
            total_chunks += n

    elapsed = time.time() - t0
    total_mem = len(m.get_all(user_id=USER_ID) or []) if m else "(dry run)"
    print(f"\n[bridge] {total_files} files | {total_chunks} chunks | {elapsed:.1f}s")
    print(f"[mem0]   Total memories: {total_mem}")


if __name__ == "__main__":
    main()
