# jOY Events: Architectural Blueprint
**Status:** Architect-Grade (Ready for Sign-off)
**Version:** 1.0
**Target Regions:** Brisbane & Gold Coast

## 1. Vision & Strategic Objective
jOY Events is a **High-Trust Discovery Engine**. Its mission is to solve the "Paradox of Choice" in the Brisbane and Gold Coast markets by providing a curated, automated, and vibe-aligned feed of what actually matters.

## 2. Product Architecture
### 2.1 The Ingestion Engine (The "Vacuum")
- **Primary API Connectors:** Eventbrite, Humanitix, Ticketek.
- **Surface Scrapers:** BCC/GCCC Council pages, Concrete Playground, Urban List, niche suburb blogs.
- **Social Listeners:** Monitoring "Vibe-Leader" social accounts for pop-ups.
- **Direct Submission:** Zero-friction portal for local organizers.

### 2.2 The AI Cleaning Layer (The "Brain")
- **Intelligent De-duplication:** LLM-powered merging of duplicate listings from multiple sources.
- **Vibe-Tagging Engine:** Tags like *Hidden Gem, High Energy, Intimate, Family-Centric*.
- **The "Joy Bar" Filter:** Quality scoring algorithm to ensure only high-vibe events make the cut.

### 2.3 Distribution Front-end (The "Delivery")
- **Web Interface:** Map-centric discovery focused on "What's on Now".
- **Personalized Alerts:** "Vibe-Match" (SMS/Push) and weekly curated digests.

## 3. The 'Trust' Protocol
1. **Editorial Firewall:** No paid listings in organic discovery.
2. **Source Transparency:** Clear display of data provenance.
3. **Community Vibe-Check:** User feedback loops to verify tag accuracy.
4. **The "No-Noise" Promise:** Quality over quantity.

## 4. Monetization Engine
- **B2B:** SaaS licensing for Hotels/Airbnbs ($49-$199/mo).
- **B2C:** Premium alerts and concierge access ($9.99/mo).
- **Revenue Potential:** High-margin tourism "middleware" owning discovery intent.

## 5. Execution Roadmap
- **Phase 1: The Pilot (Weeks 1-6):** Brisbane MVP focusing on core ingestion and manual vibe-training.
- **Phase 2: Personalization (Weeks 7-14):** AI Automation & Gold Coast rollout.
- **Phase 3: Scaling (Weeks 15+):** B2B & Premium launch.

## 6. Technical Stack
- **Backend:** Python (FastAPI).
- **AI:** OpenAI o1 / Gemini 1.5 Pro.
- **Frontend:** Next.js (Vercel).
- **Database:** PostgreSQL (PostGIS) + Redis.
