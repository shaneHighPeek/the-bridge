# jOY Events: Phase 3 Epic Specs (Top-10 Differentiators)

## Purpose
This document converts the Top-10 differentiators into build-ready epics with:
- User story
- Success metric
- Owner
- Release criteria

Use this as the implementation queue for Phase 3.

## Implementation Status
- `Epic 2: City Pulse Timeline` -> **Shipped v1** (Now/Tonight/Weekend controls + in-feed region switching + interaction analytics).
- `Epic 6: Adaptive Feed Modes` -> **Shipped v1** (Solo Explorer, Date Night, New in Town, Family Day one-tap presets).
- `Epic 4: Trust Score` -> **Shipped v1** (event-level trust score, label, and rationale shown on featured + cards; trust analytics added).
- `Epic 10: Visitor Quickstart (48-hour mode)` -> **Shipped v1** (visitor setup modal + generated 48-hour itinerary based on region/vibe/budget/style).
- `Epic 1: Social Match Layer` -> **Shipped v1** (opt-in toggle, anonymous compatible profiles, request-connect action, privacy-safe reveal model).
- `Epic 5: Group Planning Mode` -> **Shipped v1** (shared shortlist list, vote controls, top-pick summary, copyable shortlist link).
- `Epic 3: Plan Builder (Door-to-Door)` -> **Shipped v1** (add-to-plan stop types, editable timing, save/share plan actions).
- `Epic 7: Smart Fallback Engine` -> **Shipped v1** (sold-out/weather/nearby fallback modes and contextual one-tap alternatives).
- `Epic 8: Local Culture Layer` -> **Shipped v1** (region culture cards, etiquette/safety notes, hidden gem highlights, toggle control).
- `Epic 9: Post-Event Learning Loop` -> **Shipped v1** (feedback persistence + ranking adjustment from user history, including similar-match dampening).

---

## Epic 1: Social Match Layer
**User story:** As a solo attendee, I want to see compatible people attending an event so I feel safer and less isolated.  
**Success metric:** At least 20% of solo-mode users open Social Match for an event detail view.  
**Owner:** Windsurf (UI/flow), Klor (matching logic/data), Shane (trust settings).  
**Release criteria:**
- Opt-in toggle for Social Match in settings.
- “Who else is going” block on event cards/details.
- Match criteria uses vibe, region, and event intent.
- Privacy-safe defaults (anonymous until user accepts connect).
- Analytics events: `social_match_view`, `social_match_connect_click`.

## Epic 2: City Pulse Timeline
**User story:** As a curious local, I want to scan what is peaking now/tonight/weekend so I can decide quickly.  
**Success metric:** 30% of active users interact with at least one Pulse timeline control per session.  
**Owner:** Windsurf (UI), Klor (hotness feed), Shane (ranking rules).  
**Release criteria:**
- Time slider with `Now`, `Tonight`, `Weekend`.
- Region switch for Brisbane/GC/SC in timeline context.
- Pulse ranking uses Hot Meter + freshness weighting.
- Empty states handled cleanly.
- Analytics event: `city_pulse_interaction`.

## Epic 3: Plan Builder (Door-to-Door)
**User story:** As a user planning a day out, I want a multi-stop route so I can go from A to B with great stops in between.  
**Success metric:** 10% of users who open Plan Builder save a 2+ stop itinerary.  
**Owner:** Windsurf (flow/UI), Klor (routing data integration), Shane (experience design).  
**Release criteria:**
- Add-to-plan from event cards.
- Stop types: food, event, after-spot.
- Basic order + timing view.
- Save/share itinerary action.
- Analytics events: `plan_builder_open`, `plan_saved`.

## Epic 4: Trust Score
**User story:** As a cautious user, I want a trust score so I can avoid low-quality events.  
**Success metric:** 25% reduction in negative post-event feedback for low-score events after ranking changes.  
**Owner:** Klor (scoring signals), Windsurf (display), Shane (trust policy).  
**Release criteria:**
- Trust score label and explanation visible.
- Inputs include source reliability, freshness, and feedback confidence.
- Events below threshold de-prioritised or flagged.
- Tooltips explain why a score is high/low.
- Analytics event: `trust_score_view`.

## Epic 5: Group Planning Mode
**User story:** As part of a friend group, I want to vote on options so we can decide faster.  
**Success metric:** 15% of shared plans receive at least one vote from another user.  
**Owner:** Windsurf (group UI), Klor (state/presence helpers), Shane (group UX policy).  
**Release criteria:**
- Create shared shortlist link.
- Voting options (yes/no/maybe).
- Automatic top pick summary.
- Group state updates reflected in UI.
- Analytics events: `group_plan_created`, `group_vote_cast`.

## Epic 6: Adaptive Feed Modes
**User story:** As a user with different moods, I want one-tap modes so I can get relevant suggestions instantly.  
**Success metric:** 40% of sessions use at least one adaptive mode preset.  
**Owner:** Windsurf (mode UX), Shane (preset strategy), Klor (mode weighting inputs).  
**Release criteria:**
- Presets: Solo Explorer, Date Night, New in Town, Family Day.
- Mode selection updates ranking and filters in one action.
- Mode can be edited and saved to profile.
- Clear indicator of active mode.
- Analytics event: `adaptive_mode_selected`.

## Epic 7: Smart Fallback Engine
**User story:** As a user whose plan changes, I want instant alternatives so momentum is not lost.  
**Success metric:** 20% of fallback clicks result in a ticket/outbound click within the same session.  
**Owner:** Windsurf (fallback UX), Klor (recommendation logic), Shane (quality bar).  
**Release criteria:**
- Trigger types: sold out, weather, nearby.
- One-tap fallback suggestions displayed contextually.
- Fallback relevance weighted by vibe + radius + timing.
- No dead-end state in fallback flows.
- Analytics event: `fallback_reco_click`.

## Epic 8: Local Culture Layer
**User story:** As a newcomer, I want local context so I feel welcomed and culturally aware.  
**Success metric:** 15% increase in repeat visits from new users who view local culture modules.  
**Owner:** Shane (editorial direction), Windsurf (UX placement), Klor (content ops).  
**Release criteria:**
- Region culture cards with neighbourhood tone.
- “Good to know” micro-notes (etiquette/safety/local vibe).
- Hidden gem highlights integrated into feed.
- Culture layer can be toggled on/off.
- Analytics event: `culture_layer_view`.

## Epic 9: Post-Event Learning Loop
**User story:** As a user, I want my feedback to improve future recommendations so the app gets smarter for me.  
**Success metric:** 30% of users who save events submit at least one feedback action.  
**Owner:** Windsurf (feedback UX), Klor (feedback weighting model), Shane (quality thresholds).  
**Release criteria:**
- Feedback capture on event cards/details.
- Feedback written to persistent store.
- Ranking adjusts based on user feedback history.
- Negative feedback reduces similar weak matches.
- Analytics event: `event_feedback_submit`.

## Epic 10: Visitor Quickstart (48-Hour Mode)
**User story:** As a visitor, I want a ready plan in 2 minutes so I can enjoy SEQ without research overload.  
**Success metric:** 25% of visitor-mode users complete a quickstart itinerary.  
**Owner:** Windsurf (onboarding UX), Klor (visitor templates), Shane (visitor positioning).  
**Release criteria:**
- Quickstart entry on first run.
- Inputs: region, vibe, budget, travel style.
- Auto-generated 48-hour plan with optional edits.
- Clear CTA to save/share/export plan.
- Analytics events: `visitor_mode_start`, `visitor_plan_generated`.

---

## Prioritisation Order (Recommended)
1. Epic 6 (Adaptive Feed Modes)
2. Epic 2 (City Pulse Timeline)
3. Epic 7 (Smart Fallback Engine)
4. Epic 10 (Visitor Quickstart)
5. Epic 9 (Post-Event Learning Loop)
6. Epic 4 (Trust Score)
7. Epic 1 (Social Match Layer)
8. Epic 5 (Group Planning Mode)
9. Epic 3 (Plan Builder)
10. Epic 8 (Local Culture Layer)

This order maximises early user impact and learning velocity.
