# jOY Events: System Architecture & Developer Guide

This document is the "Source of Truth" for how jOY Events is built, connected, and operated. 

**STRICT RULE:** Do not alter the physical "Handset Bezel" or the "POV Perspective" without explicit Architect sign-off. These are Protected Design States.

---

## 🏗️ The Three-Layer Architecture

jOY Events operates as a decoupled system across three primary layers:

### 1. The Vacuum (Ingestion Engine - Python)
- **Location:** `shaneHighPeek/joy-events`
- **Role:** Scrapes and fetches raw data from SEQ sources.
- **Connectors:** 
    - BCC Open Data API (Live)
    - Ticketmaster Discovery API (Live)
    - Ticketek / Premier Scraper (Planned)
    - Humanitix / Eventbrite API (Planned)
    - Facebook Events Social Listener (Planned)
- **Output:** Raw JSON files or Database entries for the jOY Bar.

### 2. The Brain (jOY Bar AI - Python/LLM)
- **Location:** `shaneHighPeek/joy-events/ai`
- **Role:** High-trust curation and normalization.
- **Logic:**
    - Assigns **Vibe Tags** (Hidden Gem, High Energy, etc.).
    - Maps events to **UI Themes** (Broncos Maroon, Burleigh Sunset).
    - Calculates the **Heat Meter** (Social velocity pulse).
    - Deduplicates cross-platform listings (e.g., merging a Ticketek and Facebook listing).

### 3. The Interface (Morphic Web App - Next.js)
- **Location:** `shaneHighPeek/joy-events-web`
- **Role:** Visually stunning, user-facing handset experience.
- **Hosting:** Vercel (Auto-deploy on GitHub push).
- **Core Files:**
    - `src/app/page.tsx`: The "Portal" logic and handset UI.
    - `src/app/api/events/route.ts`: The bridge between the Brain/Vacuum data and the UI.
    - `src/app/globals.css`: Tailwind configuration for the "Morphic" skins.

---

## 🛠️ How it Connects (The Data Flow)

1. **Harvest:** The Python Engine (Vacuum) runs on the VPS to sweep SEQ.
2. **Process:** The jOY Bar AI cleans the data and tags it with a "Vibe."
3. **Expose:** An internal API endpoint (on the VPS) provides the cleaned data.
4. **Render:** The Vercel Web App fetches from the API and "morphs" the UI based on the `vibe_tag`.

---

## 📋 Operational Checklists

### When performing manual work:
- [ ] **Design:** If editing `page.tsx`, ensure the `relative z-10 w-full md:max-w-[1200px]` handset container remains centered.
- [ ] **Branding:** Use only the approved theme colors (#4B001E for Broncos, #FF7E5F for Sunset).
- [ ] **Data:** If adding a new source, update the `allEvents` object in `src/app/api/events/route.ts`.
- [ ] **Mobile:** Always test the Sidebar/HUD on a small screen after a UI change.

---

## 🗺️ Roadmap & Sprint Status

### Phase 1: Structural Integrity (DONE)
- [x] Physical Handset Frame & POV backgrounds.
- [x] Zero-scroll landing layout with centered Vibe menu.
- [x] Next.js 15.1.7 security patching and Vercel deployment.

### Phase 2: Live Pulse Integration (ACTIVE)
- [x] Bridge real event data into the handset cards.
- [ ] Implement Gold Coast & Sunshine Coast Council scrapers.
- [ ] Build the "Hype Meter" visual glow for event cards.

### Phase 3: The "Invisible Fuel" (PLANNED)
- [ ] Affiliate Link Bridge (Ticketmaster/Ticketek referral wrapper).
- [ ] Automated "Vibe Forecast" YouTube Shorts generator.
- [ ] Spotify Preview integration for Music vibe.

---

## 🎨 Design Guide: Changing Backgrounds
To change the POV atmosphere, edit `src/app/page.tsx`:
1. Find the `themes` object.
2. Replace the `visual` URL for the specific mode (DEFAULT, SPORTS, etc.).
3. **Pro Tip:** Use Unsplash URLs with `auto=format&fit=crop&q=80&w=2000` for high performance.

---
*Created by KLOR for The Captain (Shane Anderson).*
