# ⚜️ Quebec Voter Compass 2026 (`quebec-voter-compass`)

An intelligent, non-partisan AI decision-assistant designed to help Quebec voters compare political party platforms for the upcoming **2026 Quebec Provincial Election**.

Powered by **Google ADK (Agent Development Kit)**, **Gemini 2.5 Flash**, **Google Cloud Firestore**, and **Agent-Driven Adaptive UI (A2UI)**.

---

## 🌟 Key Features

- **Non-Partisan Platform Comparisons**: Side-by-side objective breakdown of party promises across all 5 major provincial parties:
  - **CAQ** (*Coalition Avenir Québec*)
  - **PLQ** (*Quebec Liberal Party / Parti libéral du Québec*)
  - **QS** (*Québec Solidaire*)
  - **PQ** (*Parti Québécois*)
  - **PCQ** (*Conservative Party of Quebec / Parti conservateur du Québec*)
- **Agent-Driven Adaptive UI (A2UI)**: Outputs structured UI component surfaces (`Card`, `Column`, `Row`, `Text`) rendered dynamically in the web client.
- **Voter Priority Matcher**: Analyzes user-defined policy goals and scores alignment across party platforms.
- **One-Click Prompt Chips**: Instant shortcut buttons for popular comparison categories (Health Care, Tax Cuts, Environment & Energy, Education & Language).

---

## 🏗️ Architecture & Wired Cloud Services

- **Google Cloud Firestore**: Data store containing structured platform policy documents across 6 core categories:
  - `health-care` (RAMQ access, family doctors, ER waiting times)
  - `cost-of-living` (Income taxes, basic personal exemption, inflation relief)
  - `education` (Bill 101 in CEGEPs, physical education, infrastructure)
  - `child-care` (CPE spots, subsidies, family tax credits)
  - `economy-tariffs` (SME corporate taxes, trade, energy investments)
  - `environment-natural-resources` (Cap-and-trade carbon market, Hydro-Québec, natural resources)
- **Google ADK (Agent Development Kit)**: Orchestrates tool calls (`compare_issue_platforms`, `get_party_platform`, `find_matching_parties`) and session memory lifecycle.
- **Vertex AI / Gemini 2.5 Flash**: Underlying generative AI model (`gemini-2.5-flash`).
- **FastAPI / Uvicorn Frontend**: Lightweight Python web server hosting the interactive client application.

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.11+**
- **Google Cloud SDK** with application default credentials (`gcloud auth application-default login`)
- GCP Project with Firestore enabled

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/fattahantar-ca/quebec-voter-compass.git
   cd quebec-voter-compass
   ```

2. **Set up Python Virtual Environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r app/requirements.txt
   ```

3. **Seed Firestore Database**:
   ```bash
   GOOGLE_GENAI_USE_VERTEXAI=true python app/seed_firestore.py
   ```

4. **Run the Application Locally**:
   ```bash
   GOOGLE_GENAI_USE_VERTEXAI=true PORT=8081 python frontend/main.py
   ```

5. Open your web browser and navigate to `http://localhost:8081`.

---

## 📁 Repository Structure

```
quebec-voter-compass/
├── agents-cli-manifest.yaml   # ADK Manifest & deployment configuration
├── Dockerfile                  # Container build instructions
├── pyproject.toml              # Project dependencies & metadata
├── README.md                   # Project documentation
├── app/
│   ├── __init__.py
│   ├── agent.py               # Core ADK Agent & custom tool definitions
│   ├── a2ui_utils.py          # A2UI callback component generator
│   ├── fast_api_app.py        # ADK FastAPI entrypoint
│   ├── requirements.txt       # Python package requirements
│   └── seed_firestore.py      # Firestore platform database seeder script
└── frontend/
    ├── main.py                # FastAPI web server & chat endpoint
    └── static/
        └── index.html         # Responsive Quebec-themed UI & A2UI renderer
```

---

## 📜 License

Distributed under the Apache 2.0 License. See `LICENSE` for more information.
