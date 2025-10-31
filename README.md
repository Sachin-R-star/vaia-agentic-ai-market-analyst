# 🚀 VAIA Agentic AI Market Analyst (Gemini Implementation)

## Overview

The VAIA system is a sophisticated market research and analysis agent designed to process external data and provide strategic, data-driven insights via a robust web API. The system was successfully migrated to the **Google GenAI SDK (Gemini)** for its high performance and cost-efficiency.

---

## 🛠️ Architecture & Tech Stack

### Components

This diagram represents the flow of requests through the system's core components:

┌─────────────────────────────────────────┐ │ FastAPI Web Server │ │ │ │ ┌───────────────────────────────────┐ │ │ │ API Endpoints │ │ │ │ - /analyze (POST) │ │ │ │ - /competitor-analysis (GET) │ │ │ - /market-trend (GET) │ │ │ │ - /strategic-recommendation (POST) │ │ └───────────────────────────────────┘ │ │ │ │ │ ▼ │ │ ┌───────────────────────────────────┐ │ │ │ Agent Processor │ │ │ │ (Gemini with Structured Prompts) │ │ └───────────────────────────────────┘ │ │ │ │ │ ▼ │ │ ┌───────────────────────────────────┐ │ │ │ Google GenAI API │ │ │ (Gemini 2.5 Flash) │ │ └───────────────────────────────────┘ │ └─────────────────────────────────────────┘


| Component | Technology | Role |
| :--- | :--- | :--- |
| **AI Core** | **Gemini 2.5 Flash** | Primary LLM chosen for high speed, cost-efficiency, and predictable structured output. |
| **Framework** | FastAPI | Building the high-performance, asynchronous REST API. |
| **Configuration** | `python-dotenv` | Secure handling of API Keys via the `.env` file. |

---

## 🧠 Design Decisions (Crucial Section for Evaluation)

This section details the engineering rationale behind the agent's design, reflecting a necessity to maintain development velocity under real-world constraints.

### 1. API Choice & Rationale (Gemini Migration)

**Decision:** The project migrated from the initially planned Anthropic/OpenAI to **Google GenAI (Gemini SDK)**.

**Justification:** This decision was an **engineering-driven necessity** based on **cost-efficiency** and **free tier availability** for continuous development. Gemini 2.5 Flash was selected for its low latency, sufficient reasoning capabilities for market analysis, and strong adherence to structured system instructions, demonstrating adaptability to external constraints.

### 2. Prompt Design and Structured Output Enforcement

**Decision:** A robust, layered system message was used with explicit output structure enforcement.

**Justification:** The system prompt performs three critical roles: 1) Defines the agent's **Persona** ("VAIA, an expert analyst"), 2) Ingests the raw data directly as **System Context**, and 3) **Explicitly structures** complex output. For the `/strategic-recommendation` endpoint, the prompt strictly enforces the 5-part structure (Short-term, Medium-term, etc.), ensuring the model delivers a predictable, actionable roadmap suitable for direct client use.

### 3. Future Enhancements & Product Strategy

**Justification:** The core architecture is designed for modularity and scalability.

* **Caching:** Immediate implementation of a Redis or simple in-memory cache for the `/analyze` and `/market-trend` endpoints to reduce repetitive LLM calls and save cost/credits (directly supporting the Gemini cost rationale).
* **RAG/Vector DB:** Future integration of RAG would use Pinecone/Vertex AI Vector Search for scalable production indexing and the 512-token chunking strategy to handle large external corpora efficiently.

---

## ⚙️ Setup & Run Instructions

### Prerequisites
* Python 3.11+
* A valid Google Gemini API Key.

### Local Setup

1.  **Clone and Navigate:**
    ```bash
    git clone [Your GitHub Repository Link]
    cd vaia-agentic-ai-market-analyst
    ```
2.  **Activate Environment & Install Dependencies:**
    ```bash
    .\.venv\Scripts\activate
    pip install -r requirements.txt
    pip install python-dotenv 
    ```
3.  **Configuration (.env):**
    Create a **`.env`** file in the root directory and add your keys:
    ```dotenv
    VAIA_AGENT_API_KEY=VAIA_ASSIGNMENT_KEY_2025_SecretXyZ
    GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
    ```
4.  **Run the Application:**
    ```bash
    cd src
    uvicorn main:app --reload
    ```
5.  **Access:**
    Open API Docs at: **`http://127.0.0.1:8000/docs`**

---

## 🌐 API Endpoints (Testing Examples)

**Note:** All requests require the header **`X-Api-Key: VAIA_ASSIGNMENT_KEY_2025_SecretXyZ`**.

#### 1. Strategic Recommendations (`POST /strategic-recommendation`)

```json
{
  "query": "A large legacy retail company must shift its budget focus from physical store maintenance to online expansion. Provide a strategic roadmap.",
  "market": "Global Omnichannel Retail Market"
}
CURL Example (Corrected with Header):

Bash

curl -X POST "[http://127.0.0.1:8000/strategic-recommendation](http://127.0.0.1:8000/strategic-recommendation)" \
     -H "Content-Type: application/json" \
     -H "X-Api-Key: VAIA_ASSIGNMENT_KEY_2025_SecretXyZ" \
     -d '{ "query": "Shift budget focus from physical store maintenance to online expansion. Provide a strategic roadmap.", "market": "Global Omnichannel Retail Market" }'
2. General Market Analysis (POST /analyze)
JSON

{
  "query": "What are the primary risks and top three growth opportunities for a new B2B SaaS company launching in Southeast Asia?",
  "market": "Southeast Asian Logistics Tech"
}
CURL Example (Corrected with Header):

Bash

curl -X POST "[http://127.0.0.1:8000/analyze](http://127.0.0.1:8000/analyze)" \
     -H "Content-Type: application/json" \
     -H "X-Api-Key: VAIA_ASSIGNMENT_KEY_2025_SecretXyZ" \
     -d '{ "query": "What are the primary risks and top three growth opportunities for a new B2B SaaS company launching in Southeast Asia?", "market": "Southeast Asian Logistics Tech" }'
3. Competitor Analysis (GET /competitor-analysis)
Bash

# Example Query (Use browser or cURL):
curl -X GET "[http://127.0.0.1:8000/competitor-analysis?competitor=Synergy%20Systems&market=AI%20Workflow%20Automation](http://127.0.0.1:8000/competitor-analysis?competitor=Synergy%20Systems&market=AI%20Workflow%20Automation)" \
     -H "X-Api-Key: VAIA_ASSIGNMENT_KEY_2025_SecretXyZ"
Author: Sachin-R-star
