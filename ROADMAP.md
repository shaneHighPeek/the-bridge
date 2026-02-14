# OpenClaw Roadmap (Shane + Klor)

Timezone: Australia/Brisbane (Gold Coast, AEST UTC+10)

## Guiding principles
- **One human, one assistant**: prioritize reliability + predictable routing over cleverness.
- **Low blast radius**: change one variable at a time; verify with a test message after each change.
- **No lockouts**: avoid configs that can prevent workspace/file access.
- **Prefer config over ad-hoc**: make behavior persistent and auditable.

---

## Phase 0 — Stabilize + guardrails (do this before expanding scope)
**Goal:** prevent a repeat of “sandbox shuts us out of files”.

### 0.1 Capture current baseline
- Save current config snapshot (so we can revert quickly):
  - `openclaw gateway config get` (or via Control UI export)
- Record OpenClaw version + host info.

### 0.2 Sandbox / workspace access policy (critical)
Decide and set:
- Whether sandbox runs are used at all.
- If used: ensure **workspaceAccess** is not `none` for the sessions where we need files.

Recommended default for a single-user setup:
- Sandbox: **off** initially (until everything is stable), OR
- Sandbox: **non-main** with **workspaceAccess: rw** for main, and RO for subagents if desired.

Verification test:
- Ask Klor to read/write a small file in `/data/.openclaw/workspace/`.

### 0.3 Secrets hygiene (token safety)
- Telegram bot token must never be pasted into shared chats.
- Store tokens only in OpenClaw config (sensitive fields) or env vars.
- If a token is ever pasted, immediately revoke/rotate via BotFather.

---

## Phase 1 — Telegram groups: make it reliable
**Goal:** Klor responds in **DMs and all your Telegram groups**, without mention-gating, since it’s only you.

### 1.1 Enable groups in a safe way
- Keep **groupPolicy = allowlist** (recommended) so only you can trigger in groups.
- Set **groupAllowFrom = [<ShaneTelegramUserId>]**.
- Allow groups:
  - Easiest: `channels.telegram.groups: { "*": { requireMention: false } }`
  - Or stricter: list explicit group IDs.

Telegram-side requirement:
- If the bot must receive all group messages, ensure BotFather privacy mode is OFF:
  - @BotFather → `/setprivacy` → **Disable**
  - Then remove + re-add the bot to each group.

### 1.2 Get group chat IDs
We need each group’s `chat.id` (negative `-100...`).
- Run `openclaw logs --follow --plain | grep -Ei "telegram|chat\\.id|\"chat\""`
- Send `id test` in each group
- Copy the `-100...` ids.

### 1.3 Routing model/agent per group (your desired split)
You want 3 groups with different “default brains”:
- **KLOR | Planning** → Gemini (main)
- **KLOR | Automation** → Gemini (main)
- **KLOR | Coding** → Claude (coding only)
- **Bridge/strategy** → OpenAI (ChatGPT 5.2) to coordinate between them

Implementation options:
- **Option A (simple):** one agent, use `/model` commands per group/session.
- **Option B (recommended):** create **3 agents** with fixed models and bind each Telegram group to the right agent.

We will do Option B.

Acceptance tests:
- In each group: send “ping” → confirm response.
- In Coding group: ask a coding task → confirm Claude is used.
- In Planning group: ask a planning task → confirm Gemini is used.

---

## Phase 2 — Import prior .md files (fast-track context)
**Goal:** migrate your old OpenClaw context safely.

### 2.1 What to copy in
From the old install, gather:
- `SOUL.md`, `USER.md`, `IDENTITY.md`
- `MEMORY.md`
- `memory/*.md`
- any custom docs you used (e.g. `TOOLS.md`, `HEARTBEAT.md`, project notes)

### 2.2 How to deliver
- Zip them or paste file contents in chunks.
- We’ll store them under `workspace/imports/<date>/...` first (non-destructive).

### 2.3 Merge strategy
- Diff old vs new.
- Merge only what’s valuable into current `USER.md`, `IDENTITY.md`, and `MEMORY.md`.
- Keep a changelog.

---

## Phase 3 — Security review + hardening (before more integrations)
**Goal:** avoid exposure + prevent self-inflicted outages.

Checklist:
- Gateway bind mode (loopback vs LAN vs tailnet)
- Auth mode (token/password), rotate tokens
- Control UI security (`allowInsecureAuth`)
- Plugin exposure (only enable what you use)
- Least-privilege tool policy (exec/message/cross-context sends)
- Backup/rollback plan for config

Deliverables:
- A “known-good” config snapshot
- A rollback procedure
- A periodic healthcheck (optional cron)

---

## Phase 4 — Automation and workflows
After Telegram + security are stable:
- Add automation tasks (reminders, checklists, structured workflows)
- Decide which surfaces get proactive messages (Telegram only at first)

---

## Next actions (when you’re back)
1) Decide sandbox posture (off vs non-main) and confirm workspace access.
2) Enable Telegram group allowlist + requireMention=false.
3) Pull group chat IDs for the 3 groups.
4) Create agents + bind groups to the right agent/model.
5) Import old .md files into `imports/` and merge.
6) Run security hardening pass.
