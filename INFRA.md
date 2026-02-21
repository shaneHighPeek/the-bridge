# INFRA.md - Infrastructure & Safety Rules (Klor)

This is the authoritative operating policy for the Klor deployment. All agents must follow these rules without exception.

## Architecture Context
- **Host:** Hostinger VPS (Ubuntu)
- **Docker Project Path:** `/opt/klor`
- **Container Name:** `openclaw-y5he-openclaw-1`
- **Dashboard:** `http://100.103.129.112:44326/` (Tailscale-only)
- **Gateway:** Listens on loopback (127.0.0.1), NOT publicly bound.

## Critical Safety Rules
1. **NO `openclaw onboard`:** Never run this command. It breaks networking and Telegram.
2. **NO Port Changes:** Do not modify `gateway.port`, bind addresses, or Docker networking.
3. **NO Manual `openclaw.json` Edits:** Unless explicitly approved by the operator.
4. **NO Environment UI:** Avoid the Hostinger UI environment editor for live containers.

## Mandatory Execution Rule (The Node Rule)
Any command that writes files to `/data/.openclaw/` **MUST** be executed as user `node`.
- **Correct Pattern:** `sudo docker exec -u node -it openclaw-y5he-openclaw-1 sh -lc "<command>"`
- **Why:** Running as root flips file ownership to `root:root`, causing `EACCES` errors and crashing the gateway.

## Verification Loop
After any change, perform these checks:
1. **Dashboard:** `curl -Is http://100.103.129.112:44326/ | head -n 1` (Expect 200 OK)
2. **Logs:** `sudo docker logs --since 3m openclaw-y5he-openclaw-1 2>&1 | grep -iE "error|exception|fail"`
3. **Ownership:** `sudo docker exec openclaw-y5he-openclaw-1 ls -la /data/.openclaw/openclaw.json` (Must be `node:node`)

## Secrets
- Never print tokens, API keys, or OAuth codes in logs.
- If the operator shares a secret, acknowledge it but do not repeat it.
