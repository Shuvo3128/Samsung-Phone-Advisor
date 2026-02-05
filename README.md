#  Samsung Phone Advisor

An AI-powered Samsung smartphone advisor that helps users explore phone specifications, compare models, and get recommendations using **PostgreSQL + SQL-based RAG + Multi-Agent System + Local LLM (Ollama)**.

This project demonstrates a **production-style AI assistant architecture** built with FastAPI and Streamlit.

---

##  Features

- Get detailed specs of Samsung smartphones  
- Compare two Samsung phones (camera, battery, performance, etc.)  
- Recommend the best Samsung phone under a given budget  
- SQL-based RAG (Retrieval Augmented Generation)  
- Multi-Agent architecture (Data Extractor, Review Generator, Confidence Agent)  
- Clean, SaaS-style Streamlit chat UI  
- Hallucination-controlled responses (DB-first, LLM-last)

---

##  Tech Stack

- **Backend:** FastAPI  
- **Frontend:** Streamlit  
- **Database:** PostgreSQL  
- **ORM:** SQLAlchemy  
- **RAG:** SQL-based retrieval  
- **LLM:** Ollama (local model)  
- **Language:** Python  


📂 Project Structure

```text
SAMSUNG-PHONE-ADVISOR/
├── app/
│   ├── agents/
│   │   ├── greeting_agent.py        # WORKING
│   │   ├── help_agent.py            # WORKING
│   │   ├── clarification_agent.py   # WORKING
│   │   ├── fallback_agent.py        # WORKING
│   │   ├── data_extractor.py        # WORKING
│   │   ├── review_generator.py      # WORKING
│   │   ├── confidence_agent.py      # WORKING
│   │   └── agent_manager.py         # WORKING
│   ├── api/
│   │   ├── routes.py                # WORKING
│   │   ├── schemas.py               # WORKING
│   │   └── __init__.py
│   ├── core/
│   │   ├── settings.py              # WORKING
│   │   ├── database.py              # WORKING
│   │   └── config.py                # FUTURE / OPTIONAL
│   ├── models/
│   │   └── phone.py                 # WORKING
│   ├── rag/
│   │   ├── query_classifier.py      # WORKING
│   │   └── retriever.py             # WORKING
│   ├── services/
│   │   ├── comparison.py            # FUTURE
│   │   └── recommendation.py        # FUTURE
│   ├── utils/
│   │   ├── prompt_templates.py      # FUTURE
│   │   ├── text_parser.py           # FUTURE
│   │   └── create_tables.py         # WORKING
│   └── main.py                      # WORKING
├── scraper/
│   ├── gsmarena_scraper.py          # WORKING
│   ├── insert_sample_data.py        # WORKING
│   └── insert_to_db.py              # OPTIONAL
├── tests/
│   ├── test_agents.py               # FUTURE
│   └── test_api.py                  # FUTURE
├── streamlit_app.py                 # WORKING
├── requirements.txt
├── README.md
├── docker-compose.yml               # FUTURE
├── .env                             # NOT COMMITTED
└── .gitignore

---

## ⚙️ Setup Instructions

Follow the steps below to set up and run the project locally.

---

### 1️⃣ Prerequisites

Make sure you have the following installed on your system:

- Python **3.10+**
- PostgreSQL **13+**
- Git
- Ollama (for local LLM)

👉 Install Ollama from: https://ollama.com  
After installation, pull a model (example):

```bash
ollama pull llama3.2:1b


2️⃣ Clone the Repository
git clone https://github.com/your-username/samsung-phone-advisor.git
cd samsung-phone-advisor

3️⃣ Create Virtual Environment
python -m venv venv

Activate the virtual environment:

Windows

venv\Scripts\activate

4️⃣ Install Dependencies
pip install -r requirements.txt

5️⃣ Configure Environment Variables

Create a .env file in the project root:

DB_HOST=localhost
DB_PORT=5432
DB_NAME=samsung_db
DB_USER=postgres
DB_PASSWORD=postgres

6️⃣ Create Database Tables

Make sure PostgreSQL is running, then run:

python app/utils/create_tables.py


This will create the required phones table.

7️⃣ Insert Sample Phone Data

Insert 15 Samsung phones into the database:

python -m scraper.insert_sample_data


✅ This step is required for the system to return meaningful answers.

🚀 Running the Application
1️⃣ Start FastAPI Backend
uvicorn app.main:app --reload

Backend will be available at:

http://127.0.0.1:8000

Health check:

http://127.0.0.1:8000/

2️⃣ Start Streamlit Frontend

Open a new terminal (keep FastAPI running) and run:

streamlit run streamlit_app.py


Streamlit UI will open at:

http://localhost:8501

---

🧪 Example Queries

You can try the following queries in the UI:

What are the specs of Samsung Galaxy S23 Ultra?

Compare Samsung Galaxy S23 Ultra and S22 Ultra

Which Samsung phone is best under $1000?

Recommend a Samsung phone with good battery

---

System Architecture (High-Level)

User sends a natural language query

Query Classifier detects intent (spec / compare / recommend)

DataExtractorAgent retrieves data from PostgreSQL (SQL-based RAG)

ConfidenceAgent checks data reliability

ReviewGeneratorAgent (LLM) generates natural-language response

Unified answer is returned via FastAPI and displayed in Streamlit

---
🧩 Future Improvements

Vector-based RAG (hybrid search)

Advanced recommendation scoring

User preference memory

Dockerized deployment

Authentication & rate limiting
