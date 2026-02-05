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

---



## 📂 Project Structure


SSAMSUNG-PHONE-ADVISOR/
│
├── app/ # Core application logic
│ │
│ ├── agents/ # 🤖 Multi-Agent System
│ │ ├── greeting_agent.py # ✅ Handles greetings (WORKING)
│ │ ├── help_agent.py # ✅ Explains system capabilities (WORKING)
│ │ ├── clarification_agent.py # ✅ Handles ambiguous queries (WORKING)
│ │ ├── fallback_agent.py # ✅ Graceful fallback responses (WORKING)
│ │ ├── data_extractor.py # ✅ Agent 1: DB / RAG data extraction (WORKING)
│ │ ├── review_generator.py # ✅ Agent 2: LLM-based response generation (WORKING)
│ │ ├── confidence_agent.py # ✅ Confidence scoring for reliability (WORKING)
│ │ └── agent_manager.py # ✅ Central orchestrator (WORKING)
│ │
│ ├── api/ # 🌐 FastAPI layer
│ │ ├── routes.py # ✅ /api/ask endpoint (WORKING)
│ │ ├── schemas.py # ✅ Request/Response models (WORKING)
│ │ └── init.py
│ │
│ ├── core/ # ⚙️ Configuration & Database
│ │ ├── settings.py # ✅ Environment-based global settings (WORKING)
│ │ ├── database.py # ✅ PostgreSQL connection & session (WORKING)
│ │ └── config.py # 🟡 Legacy/simple config (FUTURE / OPTIONAL)
│ │
│ ├── models/ # 🗄️ Database models
│ │ └── phone.py # ✅ Phone ORM model (WORKING)
│ │
│ ├── rag/ # 🔍 SQL-based RAG
│ │ ├── query_classifier.py # ✅ Intent + entity extraction (WORKING)
│ │ └── retriever.py # ✅ SQL RAG retriever (WORKING)
│ │
│ ├── services/ # 🧩 Domain services
│ │ ├── comparison.py # 🟡 Future advanced comparison logic
│ │ └── recommendation.py # 🟡 Future recommendation scoring logic
│ │
│ ├── utils/ # 🛠️ Utilities
│ │ ├── prompt_templates.py # 🟡 Future prompt abstraction
│ │ ├── text_parser.py # 🟡 Future NLP preprocessing
│ │ └── create_tables.py # ✅ DB table creation script (WORKING)
│ │
│ └── main.py # ✅ FastAPI app entry point (WORKING)
│
├── scraper/ # 📥 Data collection
│ ├── gsmarena_scraper.py # ✅ GSMArena Samsung phone scraper (WORKING)
│ ├── insert_sample_data.py # ✅ Inserts 15 sample phones into DB (WORKING)
│ └── insert_to_db.py # 🟡 Alternate bulk insert pipeline (OPTIONAL)
│
├── tests/ # 🧪 Testing
│ ├── test_agents.py # 🟡 Future agent-level tests
│ └── test_api.py # 🟡 Future API tests
│
├── streamlit_app.py # 🎨 Streamlit UI (WORKING, POLISHED)
├── requirements.txt # 📦 Python dependencies
├── README.md # 📘 Project documentation
├── docker-compose.yml # 🟡 Future Docker deployment
├── .env # 🔐 Environment variables (NOT COMMITTED)
├── .gitignore # ✅ Git ignore rules
└── pycache/ # Python cache (ignored)

---


