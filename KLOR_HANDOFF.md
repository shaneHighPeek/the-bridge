# Klor Handoff: jOY Events Build State

## Purpose
This document is the operational handoff from Windsurf work to Klor/OpenClaw so sync and live deployment can proceed safely.

It summarises:
- what was changed
- what must not be overwritten
- new integrations and required database tables
- known issues and next actions

---

## Scope of Work Completed
The following has been implemented in `the-bridge/joy-events-app/`:

### Phase 1 (Launchable Core)
- Search and filter controls (date, vibe, price, energy, indoor/outdoor, radius).
- Vibe Setup panel with presets and editable profile controls.
- Hot Meter states (`Cold`, `Warm`, `Hot`, `Buzzing`).
- Mission and trust protocol sections in feed.
- Footer with live links to legal pages.
- `/terms` and `/privacy` pages created.
- Event fallback handling (`Venue TBC`, `Price TBC`, image fallback).

### Phase 2 (Engagement/Retention)
- Save/favourite behaviour (local + Supabase sync when signed in).
- Events Near Me Now quick action.
- Post-event feedback actions (`Vibe Matched`, `Not Quite`, `Recommend`, `Skip Next Time`) with Supabase persistence.
- Tonight/Weekend pulse strips.
- Fallback recommendation panels (sold-out, weather-safe indoor, nearby).
- Notification intent capture module (email + region + vibe + intent types).

### Phase 3 (Differentiators, v1)
- Epic 1: Social Match Layer (opt-in, anonymous matches, request connect).
- Epic 2: City Pulse Timeline (Now/Tonight/Weekend + in-feed region controls).
- Epic 3: Plan Builder (Food/Event/After stops, timing edits, save/share).
- Epic 4: Trust Score (score + label + reason visible on cards and featured).
- Epic 5: Group Planning (shortlist, voting, top-pick summary, share link).
- Epic 6: Adaptive Feed Modes (Solo Explorer, Date Night, New in Town, Family Day).
- Epic 7: Smart Fallback Engine (mode controls + contextual alternatives).
- Epic 8: Local Culture Layer (region culture notes, etiquette, safety, hidden gems).
- Epic 9: Post-Event Learning Loop ranking influence from user feedback.
- Epic 10: Visitor Quickstart 48-hour mode (modal + generated itinerary).

---

## Key Files Changed
- `joy-events-app/src/app/page.tsx` (primary implementation surface)
- `joy-events-app/src/app/layout.tsx`
- `joy-events-app/src/app/globals.css`
- `joy-events-app/src/app/terms/page.tsx`
- `joy-events-app/src/app/privacy/page.tsx`
- `joy-events-app/src/lib/supabase.ts`
- `joy-events-app/package.json`
- `joy-events-app/package-lock.json`
- `joy-events-app/public/brisbane.png`
- `joy-events-app/public/gold-coast.png`
- `joy-events-app/public/sunshine-coast.png`
- `jOY_Events_Level4_Phased_Strategy.md`
- `jOY_Events_Phase3_Epics.md`

---

## Non-Negotiable Boundaries
Klor should preserve these boundaries:

1. Do not modify core identity/system files:
- `SOUL.md`, `MEMORY.md`, `COMPASSION.md`, `MODES.md`, `IDENTITY.md`, `AGENTS.md`, `TOOLS.md`, `memory/*.md`

2. Do not overwrite Windsurf app logic in `joy-events-app/src/app/page.tsx` unless explicitly coordinating feature changes.

3. Continue to allow overwrite of:
- `joy-events-app/src/data/events.json` (data sync output from Vacuum)

4. Keep `joy-events-app/src/app/api/events/route.ts` stable as the data bridge.

---

## Supabase Integration (New Connection)
Windsurf introduced Supabase client usage in frontend.

### Required env vars (`joy-events-app/.env.local`)
- `NEXT_PUBLIC_SUPABASE_URL`
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`

### Tables expected by current UI
- `profiles`
- `user_preferences`
- `saved_events`
- `event_feedback`
- `notification_intents` (new for notification intent capture)

If `notification_intents` does not exist, inserts from notification module will fail with user-facing message.

### `notification_intents` SQL (required if missing)
```sql
create table if not exists public.notification_intents (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users(id) on delete set null,
  email text not null,
  region text,
  vibe text,
  intent_types text[] not null default '{}',
  created_at timestamptz not null default now()
);

alter table public.notification_intents enable row level security;

create policy "notification_insert_public"
on public.notification_intents
for insert
with check (true);

create policy "notification_select_own"
on public.notification_intents
for select
using (auth.uid() = user_id);
```

---

## Known Issues / Notes
1. Desktop handset seam is improved but still noted as a polish item by user.
2. Local event volume may appear low if fallback has minimal records and live harvest is not present.
3. Magic-link auth UX now includes loading feedback.
4. Default build in this environment used `--webpack` for reliability; user machine has successfully run normal `npm run build`.

---

## Live Sync Procedure for Klor
1. Pull latest `the-bridge/main`.
2. Confirm `joy-events-app` build passes.
3. Ensure Supabase env vars and table readiness (especially `notification_intents`).
4. Run real-data test on live event feed.
5. Mirror `joy-events-app/` to `joy-events-web` repo and trigger Vercel.
6. Verify core flows on live:
- event feed and filters
- save + feedback persistence
- visitor quickstart
- trust score display
- group/social modules do not error

---

## Ownership Going Forward
- Windsurf: UI/UX feature iteration and frontend modules.
- Klor: data pipeline integrity, sync/deploy orchestration, live data verification, and operational automation.
- Shared: maintain strict source-of-truth boundaries and avoid cross-overwrites.
