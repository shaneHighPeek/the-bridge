# jOY Events: Architectural Blueprint
**Status:** Architect-Grade (Ready for Sign-off)  
**Version:** 1.0  
**Target Regions:** Brisbane & Gold Coast  
**Author:** Klor (via OpenClaw)

---

## 1. Vision & Strategic Objective
jOY Events is not another event directory; it is a **High-Trust Discovery Engine**. Its mission is to solve the "Paradox of Choice" in the Brisbane and Gold Coast markets by providing a curated, automated, and vibe-aligned feed of what actually matters. 

The goal is to move from **Search** (user work) to **Discovery** (system delivery), maintaining a "Google of Events" feel—authoritative, clean, and unbiased.

---

## 2. Product Architecture

### 2.1 The Ingestion Engine (The "Vacuum")
To achieve comprehensive coverage without manual entry, the engine must ingest data from fragmented sources:
- **Primary API Connectors:** Eventbrite, Humanitix, Ticketek, and Facebook Events (via Scraper).
- **Surface Scrapers:** Periodic "swipes" of BCC/GCCC Council pages, Concrete Playground, Urban List, and niche suburb blogs (e.g., West End Word).
- **Social Listeners:** Python-based monitoring of "Vibe-Leader" Instagram and TikTok accounts to capture pop-ups and underground events.
- **Direct Submission:** A "Zero-Friction" portal for local organisers to submit events, which are instantly queued for AI Cleaning.

### 2.2 The AI Cleaning Layer (The "Brain")
This is where raw data becomes jOY-grade content:
- **Intelligent De-duplication:** LLM-powered hashing that identifies the same event across multiple sources (e.g., a gig listed on both Facebook and the venue website) and merges them into a single "Golden Record".
- **Vibe-Tagging Engine:** Moving beyond "Music" or "Food". Events are tagged with multi-dimensional "Vibes" (e.g., *Hidden Gem, High Energy, Intimate, Family-Centric, Industry-Only*).
- **The "Joy Bar" Filter:** A quality scoring algorithm based on organiser reputation, venue history, and description quality. Events below the threshold are discarded or flagged for human review.
- **Auto-Summarisation:** Generating 2-sentence "Why go?" summaries that cut through the marketing fluff.

### 2.3 Distribution Front-end (The "Delivery")
- **Web Interface:** A blazing-fast, mobile-first SPA (Single Page Application). Focus on "What's on Now" and "What's on This Weekend" with map-based discovery.
- **Personalised Alerts:**
  - **Weekly Curated:** A high-vibe email digest.
  - **The "Vibe-Match" (SMS/Push):** Users "Follow" vibes, not categories. If an *Intimate Rooftop Session* is announced, they get a priority ping.
  - **Geofenced Discovery:** Optional notifications when a user enters a high-density event zone (e.g., Fortitude Valley or Surfers Paradise).

---

## 3. The 'Trust' Protocol
To maintain the "Google of Events" feel and avoid looking like a "Paid-for-Hire" site, we implement:

1.  **Editorial Firewall:** Paid placements are strictly labeled as "Partner Showcases" and never pollute the top organic "Discovery" results.
2.  **Source Transparency:** Every listing clearly displays its data source (e.g., "Sourced from BCC Council").
3.  **Community Vibe-Check:** A simple "Did this match the vibe?" feedback loop. If 3 users report "Not Family Friendly", the tag is automatically removed.
4.  **The "No-Noise" Promise:** We never list events just to fill space. If it’s not jOY-worthy, it’s not there.

---

## 4. Monetisation Engine (Value & Revenue)

### 4.1 B2B: The "Guest Experience" License
- **Target:** Hotels, Airbnbs, and Boutique Accommodations.
- **Product:** A white-labeled "Live Local Guide" widget/portal for guests.
- **Value Prop:** Eliminates the "What's on?" question for concierge/hosts. Increases guest satisfaction and local spend.
- **Model:** Monthly SaaS fee ($49 - $199/month per property/hotel).

### 4.2 B2C: The "jOY Premium" Alert Model
- **Target:** Power users, event-seekers, and locals who "hate missing out".
- **Product:** 
  - **Early Access:** 24-hour head start on boutique, limited-ticket events.
  - **Personal Concierge:** A dedicated WhatsApp/Telegram bot for instant local recommendations.
  - **Unlimited Vibe-Alerts:** Custom notifications for niche interests.
- **Model:** $9.99/month or $79/year.

### 4.3 Revenue Potential (Projection)
- **Year 1:** Focus on 100 high-end Airbnb hosts and 500 B2C Premium users in Brisbane.
- **Scaling:** Gold Coast expansion + Hotel Group partnerships.
- **Massive Value:** jOY Events becomes the "Middleware" for local tourism, owning the discovery intent.

---

## 5. Execution Roadmap

### Phase 1: The Pilot (Weeks 1-6)
- **Goal:** Launch "jOY Brisbane" MVP.
- **Focus:** Scrape Eventbrite & BCC. Basic Web UI. Manual vibe-tagging for the top 50 events/week to train the AI.
- **Success Metric:** 1,000 active weekly users.

### Phase 2: Personalisation (Weeks 7-14)
- **Goal:** Automate the "Brain".
- **Focus:** Implement LLM-based vibe-tagging and de-duplication. Launch user accounts and the "Vibe-Match" alert system. Expand to Gold Coast.
- **Success Metric:** 50% of users set up at least one Vibe Alert.

### Phase 3: Scaling & Monetisation (Weeks 15+)
- **Goal:** Revenue generation.
- **Focus:** Launch the B2B Widget for Airbnb hosts. Roll out "jOY Premium". Integrate with local ticketing APIs for affiliate revenue (secondary).
- **Success Metric:** First 50 B2B licenses signed.

---

## 6. Technical Stack Recommendations
To ensure rapid development and high scalability:
- **Backend:** Python (FastAPI) for the Ingestion Engine and AI Layer.
- **AI Processing:** OpenAI o1 or Gemini 1.5 Pro for complex de-duplication and vibe-tagging.
- **Database:** PostgreSQL (with PostGIS for location-based queries) + Redis for caching.
- **Front-end:** Next.js (for SEO and performance) hosted on Vercel.
- **Infrastructure:** Dockerized services on AWS or GCP for easy scaling of scrapers.

---

**Next Step:** Shane to review and approve the **Trust Protocol** and **Phase 1 scope**. Once signed off, we move to the Builder phase (Ingestion Engine development).
