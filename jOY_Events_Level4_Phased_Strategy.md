# jOY Events: Level 4 Phased Strategy & Execution Playbook

## Purpose
This is the practical guide to take jOY Events from early concept to must-have regional asset for South East Queensland.

Use this if you are starting today and know nothing. Follow phases in order. Finish each checklist before moving on.

---

## Product North Star
- **Mission:** Reduce loneliness by helping people find real events, real culture, and real connection across Brisbane, Gold Coast, and Sunshine Coast.
- **Positioning:** Local-first discovery engine with trust, curation, and vibe fit. No ad-noise.
- **Primary users:** Locals first, tourists second.
- **Success state:** jOY becomes the default app/site people use to decide what to do in SEQ.

---

## Non-Negotiables
- Keep the product useful and welcoming, not cluttered.
- Quality over quantity in event listings.
- Every feature must improve one of: belonging, trust, relevance, action.
- Build fast, but do not break core data flow or build stability.
- Frontend handoff standard: `npm run build` passes in `joy-events-app/`.

## Live Progress
- 2026-02-28: Phase 1 implementation started in `joy-events-app` (`page.tsx`, `layout.tsx`, `globals.css`).
- 2026-02-28: Added search, filters, Vibe Setup panel, trust/mission sections, Hot Meter states, footer/disclaimer block.
- 2026-02-28: Build validation passed via `npm run build -- --webpack` (default Turbopack build is environment-limited in this sandbox).
- 2026-02-28: Refined handset HUD alignment and redesigned location entry cards for stronger visual hierarchy.
- 2026-02-28: Captain confirmed app is running locally.
- 2026-02-28: Applied pixel correction pass to top HUD (menu inset, menu size, divider inset) to preserve iPhone frame illusion.
- 2026-02-28: Applied stronger HUD alignment pass (further menu inset, reduced menu scale, tighter header height, deeper divider inset).
- 2026-02-28: Confirmed correct local app target with temporary build marker; removed marker and switched HUD to inner safe-area layout to lock menu/divider inside frame geometry.
- 2026-02-28: Applied hard seam fix pass: shorter divider, deeper horizontal inset, smaller menu control, and vertical-centred menu anchoring.
- 2026-02-28: Added explicit responsive split: mobile full-bleed screen (no framed shell styling), desktop framed mode with seam-safe centred divider and corner masking.
- 2026-02-28: Desktop-specific seam correction: removed top divider in desktop mode and lowered HUD content within the framed safe-area.
- 2026-02-28: Added live `/terms` and `/privacy` pages with Australian/Queensland-aligned policy content and wired footer links.
- 2026-02-28: Replaced location card icon glyphs with custom city PNG assets from `joy-events-app/public/`.
- 2026-02-28: Relabelled energy language to positive UX terms (Calm, Balanced, High Energy).
- 2026-02-28: Added frontend fallback handling (`Venue TBC`, `Price TBC`) and baseline analytics hooks (`event_card_view`, `event_click`, `save_event`, `settings_complete`).
- 2026-02-28: Wired travel radius into live filtering and surfaced distance chips/labels in featured + event cards.
- 2026-02-28: Installed Supabase client and wired Phase 2 foundations: magic-link auth UI, session detection, profile upsert, preference sync, and saved-event persistence.
- 2026-02-28: Improved auth UX with loading feedback for magic-link requests (spinner + disabled button state).
- 2026-02-28: Added “Events Near Me Now” quick action (distance + timing prioritisation with one-tap toggle in filters).
- 2026-02-28: Added post-event feedback loop controls on cards with Supabase persistence to `event_feedback` and local fallback when signed out.
- 2026-02-28: Added “Tonight Pulse” and “Weekend Pulse” strips to surface hot nearby events and enable one-tap title filtering.
- 2026-02-28: Added fallback recommendation panels for sold-out, weather-safe indoor, and nearby alternatives with one-tap filter actions.
- 2026-02-28: Added notification intent capture module (email + region + vibe + intent types) with Supabase insert path and analytics tracking.
- 2026-02-28: Converted Phase 3 Top-10 differentiators into build-ready epics in `jOY_Events_Phase3_Epics.md`.
- 2026-02-28: Shipped Phase 3 differentiator v1s: Adaptive Feed Modes and City Pulse Timeline controls (with in-feed region switching + analytics hooks).
- 2026-02-28: Shipped additional Phase 3 differentiator v1s: Trust Score presentation and Visitor Quickstart 48-hour itinerary generator.
- 2026-02-28: Shipped additional Phase 3 differentiator v1s: Social Match Layer and Group Planning Mode.
- 2026-02-28: Shipped additional Phase 3 differentiator v1s: Plan Builder, Smart Fallback Engine, Local Culture Layer, and Post-Event Learning Loop upgrades.

---

## Phase 0: Foundation (Do First)
Goal: create a stable base before feature expansion.

### Checklist
- [x] Confirm project runs locally (`npm install`, `npm run dev`) in `joy-events-app`.
- [x] Confirm production build passes (`npm run build`) (validated with `--webpack` in current environment).
- [x] Audit current UI states: desktop, tablet, mobile.
- [x] Identify broken/missing pieces in:
  - [x] event cards
  - [x] theme switcher
  - [x] region selector
  - [x] settings UX
- [x] Add baseline analytics events:
  - [x] `event_card_view`
  - [x] `event_click`
  - [x] `save_event`
  - [x] `settings_complete`
- [x] Add legal footer shell (placeholder links if needed): Terms, Privacy, Disclaimer, Data Sources.

### Definition of Done
- App is stable locally and build-clean.
- Core UX gaps are documented.
- Footer/legal baseline is visible.

---

## Phase 1: Launchable Core (Must Ship)
Goal: ship a clean, trustworthy, personalised experience for BNE/GC/SC.

### Core Features
1. Region selector (Brisbane, Gold Coast, Sunshine Coast).
2. Personalised feed from onboarding preferences.
3. Clear filters and search bar.
4. Event trust signals on cards (source, time, suburb, price).
5. Hot Meter UI with placeholder score.
6. Settings flow that is fun, fast, and editable.
7. Mission visibility across key pages.
8. Footer and disclaimers complete.

### Checklist
- [x] Add top-level search bar (`keyword`, `venue`, `suburb`).
- [ ] Add quick filters:
  - [x] date/time
  - [x] vibe
  - [x] price
  - [x] distance/travel radius
  - [x] indoor/outdoor
- [x] Build onboarding as “Vibe Setup” (not boring form):
  - [x] vibe choices
  - [x] social mode (solo/date/mates/family)
  - [x] budget bands
  - [x] energy level
  - [x] travel preference
- [x] Save profile as reusable modes (`Friday Night`, `Sunday Reset`, etc.).
- [x] Add mission panel: why jOY exists and who it serves.
- [x] Finalise footer pages:
  - [x] Terms
  - [x] Privacy
  - [x] Disclaimer (events can change/cancel)
  - [x] Data source transparency
- [x] Add Hot Meter states for UI now:
  - [x] Cold
  - [x] Warm
  - [x] Hot
  - [x] Buzzing
- [x] Add fallback content handling:
  - [x] missing image
  - [x] missing price
  - [x] missing venue

### Definition of Done
- A new user can set preferences in under 2 minutes.
- Feed feels relevant on first session.
- Trust and mission are obvious.
- Build passes.

---

## Phase 2: Engagement & Retention (High-Leverage)
Goal: make users return, not just visit once.

### Checklist
- [x] Add save/favourite system.
- [x] Add “events near me now” shortcut.
- [x] Add post-event feedback loop:
  - [x] “Did this match the vibe?”
  - [x] “Would you recommend?”
- [x] Add fallback recommendations:
  - [x] sold out alternatives
  - [x] weather alternatives
  - [x] nearby alternatives
- [x] Add “tonight/weekend pulse” strips.
- [x] Add notification intent capture (email/push placeholder if infra pending).

### Definition of Done
- Users can build a lightweight habit.
- Feedback loop improves future relevance.

---

## Phase 3: Level 4 Differentiators (Top 10)
Goal: implement the features that transform jOY into a must-have asset.

These 10 must stay on roadmap and progressively ship:

1. **Social Match Layer**
- Opt-in: see who else is going, match by vibe intent.

2. **City Pulse Timeline**
- Time-slider for what is peaking now, tonight, this weekend across all 3 regions.

3. **Plan Builder (Door-to-Door)**
- Build multi-stop itineraries (train, lunch, event, after-spot).

4. **Trust Score**
- Event quality score using source reliability, freshness, and confidence.

5. **Group Planning Mode**
- Shared shortlist + voting + decision support.

6. **Adaptive Feed Modes**
- Instant presets (Solo Explorer, Date Night, New in Town, Family Day).

7. **Smart Fallback Engine**
- Auto-suggest equivalent experiences when plans fail.

8. **Local Culture Layer**
- Micro-guides for neighbourhood culture, hidden gems, and practical safety context.

9. **Post-Event Learning Loop**
- Behaviour + feedback used to refine personal recommendations.

10. **Visitor Quickstart (48-hour mode)**
- Fast setup for tourists with instant curated plan.

### Checklist
- [x] Convert each Top-10 item into epics with:
  - [x] user story
  - [x] success metric
  - [x] technical owner
  - [x] release criteria
- [x] Ship at least 2 differentiators before broad growth push.
- [x] Epic 2: City Pulse Timeline (v1 shipped).
- [x] Epic 4: Trust Score (v1 shipped).
- [x] Epic 1: Social Match Layer (v1 shipped).
- [x] Epic 5: Group Planning Mode (v1 shipped).
- [x] Epic 6: Adaptive Feed Modes (v1 shipped).
- [x] Epic 10: Visitor Quickstart (48-hour mode) (v1 shipped).
- [x] Epic 3: Plan Builder (Door-to-Door) (v1 shipped).
- [x] Epic 7: Smart Fallback Engine (v1 shipped).
- [x] Epic 8: Local Culture Layer (v1 shipped).
- [x] Epic 9: Post-Event Learning Loop (v1 shipped).

### Definition of Done
- jOY has capabilities users cannot get from generic event sites.

---

## Phase 4: Visibility Engine (SEO + Distribution)
Goal: become discoverable at scale while product quality remains high.

### Checklist
- [ ] Build SEO landing pages by:
  - [ ] region
  - [ ] suburb
  - [ ] vibe
  - [ ] time window (this weekend/tonight)
- [ ] Add structured data for events (schema markup).
- [ ] Ensure indexable event detail pages.
- [ ] Define content cadence:
  - [ ] weekly city pulse roundup
  - [ ] top hidden gems
  - [ ] what’s hot this weekend
- [ ] Social distribution plan (Klor-owned ops):
  - [ ] X/Twitter trend snippets
  - [ ] Facebook local community summaries
  - [ ] short-form recap content
- [ ] Partnerships shortlist:
  - [ ] venues
  - [ ] councils
  - [ ] local creators
  - [ ] student groups

### Definition of Done
- Organic discovery is compounding.
- Brand starts to own “what’s on in SEQ” intent.

---

## Phase 5: Revenue & Defensibility
Goal: monetise without breaking trust.

### Checklist
- [ ] Keep organic feed ad-light and clearly curated.
- [ ] Monetisation path A (B2B):
  - [ ] hospitality widget
  - [ ] concierge/local guide licence
- [ ] Monetisation path B (B2C premium):
  - [ ] advanced alerts
  - [ ] premium itinerary tools
  - [ ] insider drops
- [ ] Add transparent “partner content” labels where needed.
- [ ] Track revenue KPIs without polluting user experience.

### Definition of Done
- Revenue starts while trust remains intact.

---

## Build Order (If Starting Today)
Use this exact order for momentum:

1. Stabilise and build-check app.
2. Add search + filters.
3. Rebuild settings as fast/fun onboarding.
4. Add trust signals + mission + footer/disclaimers.
5. Add Hot Meter UI states and card polish.
6. Add save/favourite + post-event feedback.
7. Start SEO page system and schema.
8. Begin Top-10 differentiators (start with #2 City Pulse + #6 Adaptive Modes).
9. Add Plan Builder foundation.
10. Prepare monetisation rails (without clutter).

---

## Decision Filter (Use Before Any New Feature)
Before building, ask:

1. Does this reduce loneliness or increase belonging?
2. Does this improve trust or relevance?
3. Does this make action easier right now?
4. Can this ship cleanly without breaking build?
5. Is this core-now or expansion-later?

If answer is mostly “no”, park it.

---

## Logical End Point (Current Vision)
The logical end point is not “finished code”. It is:
- The most trusted “what’s on” and “where do I belong tonight” product for SEQ.
- Strong local habit for residents.
- Strong onboarding for visitors.
- Clear path to own attention heading into Brisbane 2032.

This is the bar for Level 4.
