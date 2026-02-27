# jOY Events: System Architecture & Windsurf Context

## 1. Overview
This file provides context for any AI assistant (Windsurf/Cascade) operating within **The Bridge** (Mission Control). It explains how jOY Events is structured, how the data flows, and the boundaries between local development and live deployment.

## 2. Repository Structure
You are currently inside `the-bridge`. This is the central workspace.

### **Local Folders (The Factory)**
- **`joy-events/`**: The "Vacuum" (Backend/Scrapers).
  - Contains Python scrapers (BCC, GCCC, etc.) that harvest event data.
  - **Goal**: Generate `events.json`.
- **`joy-events-app/`**: The Frontend (Next.js/React).
  - This is where you edit the UI, themes (SPORTS, MUSIC, CHILL), and API routes.
  - **Data Source**: It reads from `src/data/events.json`.

### **External Repository (The Live Site)**
- **`shaneHighPeek/joy-events-web`**: This is a standalone, lean repo.
  - **DO NOT** edit this directly unless instructed. 
  - Klor (the OpenClaw agent) automatically syncs `joy-events-app/` to this repo to trigger Vercel deployments at `joy-events-web.vercel.app`.

## 3. Data Flow (How it Interlinks)
1. **Harvest**: Python scripts in `joy-events/` scrape data and save it to `joy-events/data/events.json`.
2. **Sync**: The data is copied/imported into `joy-events-app/src/data/events.json`.
3. **Display**: The Next.js API (`src/app/api/events/route.ts`) reads that JSON file and serves it to the frontend.
4. **Deploy**: Klor pushes the `joy-events-app/` content to the `joy-events-web` GitHub repo, which Vercel builds and hosts.

## 4. Boundaries & Constraints
- **The Bridge Files**: Do not touch `SOUL.md`, `MEMORY.md`, or `COMPASSION.md` unless explicitly asked by the Captain. These are core identity files for the OpenClaw system.
- **Environment Variables**: API keys (Ticketmaster, etc.) live in `.env` files which are git-ignored. Check with the Captain if they are missing.
- **Vercel**: Vercel is connected only to the `joy-events-web` repo, not to `the-bridge`.

## 5. Current Priorities for Windsurf
- **UI/UX Refinement**: Improving the "Handset" aesthetic and event card layouts.
- **Theme Logic**: Ensuring the vibe-switcher (SPORTS, MUSIC, CHILL) feels high-trust and premium.
- **Mapping**: Ensuring event imagery correctly maps to the cards.

---
**Last Updated**: 2026-02-28
**Co-pilot**: Klor ⚡