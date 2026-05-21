# Claimpilot: AI Insurance Assistant

An enterprise-grade, end-to-end AI automation pipeline for processing insurance claims. Claimpilot features a multimodal vision extractor, an autonomous decision-making agent, and a Human-in-the-Loop (HITL) UI for edge-case resolution.

## 🚀 Core Features
* **Multimodal Vision Pipeline:** Extracts structured data (Amount, Date, Provider) from raw receipts and PDF invoices using Google Gemini 2.5 Flash.
* **Autonomous Decision Engine:** A stateful LangGraph agent that evaluates claims against strict business rules (e.g., Straight-Through Processing for claims < $20k).
* **Human-in-the-Loop UI:** A dynamic Streamlit frontend that automatically halts processing and requests human authorization for high-value claims.
* **Permanent Memory:** SQLite database integration for reading and writing claim statuses via custom agent tools.

## 🛠️ Tech Stack
* **Frontend:** Streamlit
* **Backend:** FastAPI, Uvicorn
* **AI / LLM:** LangChain, LangGraph, Google Gemini 2.5 Flash
* **Database:** SQLite3

## ⚙️ Installation & Setup

**1. Clone the repository**
```bash
git clone https://github.com/sgjadhav/Claimpilot.git
cd Claimpilot
```

**2. Set up the virtual environment & install dependencies**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

**3. Configure API Keys**
Create a `.env` file in the root directory and add your Google Gemini API key:
```text
GEMINI_API_KEY=your_api_key_here
```

**4. Run the Application (Requires two terminals)**
*Terminal 1 (Backend):*
```bash
cd backend
uvicorn main:app --reload
```
*Terminal 2 (Frontend):*
```bash
cd frontend
streamlit run app.py
```
