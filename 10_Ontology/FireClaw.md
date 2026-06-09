# FireClaw — Hot-Line in the Claw Taxonomy

> UrantiOS governed. Truth · Beauty · Goodness.

## Definition

**FireClaw** is the *hot line* of the constellation: a local forwarder that
transmits urgent signals from the edge (iPhone, iMac, LobsterBot, Claude
sessions) to the Council on NemoClaw.

FireClaw does **not** decide. It **relays**. The Word (The Council) decides.
The Lucifer Test applies — every signal is logged, every forward reported
honestly, every failure counted.

## Position

```
 edge agents ──► FireClaw (127.0.0.1:8797) ──► NemoClaw (n8n on OpenClaw)
                  │                              │
                  └── local log                  └── Council of Seven
```

| Claw      | Ontological role                              |
| --------- | --------------------------------------------- |
| OpenClaw  | The *Place* — execution ground (Hetzner)      |
| NemoClaw  | The *Word* — workflow logic (n8n)             |
| NanoClaw  | The *Many* — edge fleet                       |
| FireClaw  | The *Cry* — urgent signal transport           |
| URANTiOS  | The *Memory* — ontology & the Book            |

## Mandate

- Never act beyond forwarding.
- Never drop a signal silently — count failures, expose them on `/health`.
- Never bind to non-loopback interfaces without an explicit `FIRECLAW_TOKEN`.
- Every signal carries: `source`, `severity`, `message`, `meta`, `id`,
  `received_at`.

## See

- `setup/fireclaw/` in `mircea-constellation` — implementation.
- `pipeline/fireclaw.md` in `urantios` — how the signal enters the pipeline.
