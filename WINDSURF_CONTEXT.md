# jOY Events: System Architecture & Windsurf Context

## 1. Source of Truth
- **Mission Control / System Docs**: Root of `the-bridge` (e.g., `SOUL.md`, `MEMORY.md`, `COMPASSION.md`).
- **The Vacuum (Backend)**: `the-bridge/joy-events/` (Python scrapers + data harvesting).
- **The Web App (Frontend)**: `the-bridge/joy-events-app/` (Next.js source code).
- **Live Production**: `shaneHighPeek/joy-events-web` (External repo; mirrored from `joy-events-app/`).

## 2. Boundaries & Restrictions
### **DO NOT EDIT (OpenClaw / Klor Territory)**
- `the-bridge/SOUL.md`, `MEMORY.md`, `COMPASSION.md`, `MODES.md`, `IDENTITY.md`.
- `the-bridge/AGENTS.md`, `TOOLS.md`.
- `the-bridge/memory/*.md`.
These are core identity and operational files for the OpenClaw agent.

### **AUTO-GENERATED / OVERWRITTEN**
- `the-bridge/joy-events-app/src/data/events.json`: OpenClaw overwrites this when syncing new harvests from the Vacuum.
- `the-bridge/WINDSURF_CONTEXT.md`: OpenClaw maintains this for system orientation.

## 3. Sync & Commit Workflow
- **Commit Strategy**: Work and commit **ONLY** within `the-bridge`. 
- **The Sync**: Klor (OpenClaw) manages the extraction of `joy-events-app/` and force-pushes it to the external `joy-events-web` repo to trigger Vercel. 
- **Developer Rule**: Do not initialize separate git repositories inside `joy-events-app/` or `joy-events/`. Stay within the single `the-bridge` git tree.

## 4. Conflict Protocol
- **Klor Wins on Identity**: If an AI edits `SOUL.md` or `MEMORY.md`, Klor will revert and flag it.
- **You Win on UI/UX**: Klor will not touch `joy-events-app/src/` (except for the data file) while you are in a "Play" session.
- **Merge Strategy**: Manual merge via Klor. If you make heavy changes, tell Klor "Sync these changes live" and Klor will handle the mirror update.

## 5. Validation & Handoff
- **Checklist before handoff to Klor**:
  1. `npm run build` (inside `joy-events-app`) must pass.
  2. No breaking changes to `src/app/api/events/route.ts` (this is the data bridge).
  3. All new images must have high-trust fallbacks.
- **Handover Command**: Tell Klor: *"UI changes are committed in The Bridge. Sync them to the live site."*

---
**Status**: Ready for Windsurf Operations.
**Co-pilot**: Klor ⚡