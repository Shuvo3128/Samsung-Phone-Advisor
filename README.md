📱 Samsung Phone Advisor

An AI-powered Samsung smartphone advisor that helps users explore phone specifications, compare models, and receive intelligent recommendations using a SQL-based RAG pipeline and a multi-agent system.

This project demonstrates a production-style AI assistant architecture built with FastAPI, PostgreSQL, Streamlit, and a local LLM (Ollama).

🚀 Key Capabilities

🔍 Retrieve detailed Samsung phone specifications from a database

⚖️ Compare two Samsung smartphones (camera, battery, performance, etc.)

💸 Recommend the best Samsung phone under a given budget

🧠 SQL-based Retrieval Augmented Generation (RAG)

🤖 Multi-Agent architecture for modular reasoning

🧾 Hallucination-controlled responses (DB-first, LLM-last)

🖥️ Clean, SaaS-style Streamlit chat interface

🧠 System Architecture (High Level)
User Query
   ↓
Query Classifier
   ↓
Agent Manager
   ↓
Relevant Agent (Data / Review / Help / Fallback)
   ↓
SQL-based Retriever (PostgreSQL)
   ↓
LLM (Ollama)
   ↓
Confidence Agent
   ↓
Final Response

🧩 Multi-Agent Design
Agent	Responsibility
Greeting Agent	Handles greetings and welcome messages
Help Agent	Explains system capabilities
Clarification Agent	Requests missing information
Data Extractor Agent	Retrieves phone specs from DB
Review Generator Agent	Generates natural-language reviews
Confidence Agent	Scores response reliability
Fallback Agent	Handles unknown or unsupported queries
Agent Manager	Routes queries to the correct agent
🧠 RAG Strategy

Retrieval: SQL-based querying over PostgreSQL (no vector hallucination)

Generation: LLM is used only after verified data retrieval

Control: Ensures factual, grounded responses

🛠️ Tech Stack
Layer	Technology
Backend API	FastAPI
Frontend UI	Streamlit
Database	PostgreSQL
ORM	SQLAlchemy
RAG	SQL-based Retrieval
LLM	Ollama (Local Model)
Language	Python
📂 Project Structure
SAMSUNG-PHONE-ADVISOR/
├── app/
│   ├── agents/
│   │   ├── greeting_agent.py
│   │   ├── help_agent.py
│   │   ├── clarification_agent.py
│   │   ├── fallback_agent.py
│   │   ├── data_extractor.py
│   │   ├── review_generator.py
│   │   ├── confidence_agent.py
│   │   └── agent_manager.py
│   │
│   ├── api/
│   │   ├── routes.py
│   │   ├── schemas.py
│   │   └── __init__.py
│   │
│   ├── core/
│   │   ├── settings.py
│   │   ├── database.py
│   │   └── config.py
│   │
│   ├── models/
│   │   └── phone.py
│   │
│   ├── rag/
│   │   ├── query_classifier.py
│   │   └── retriever.py
│   │
│   ├── services/
│   │   ├── comparison.py
│   │   └── recommendation.py
│   │
│   ├── utils/
│   │   ├── prompt_templates.py
│   │   ├── text_parser.py
│   │   └── create_tables.py
│   │
│   └── main.py
│
├── scraper/
│   ├── gsmarena_scraper.py
│   ├── insert_sample_data.py
│   └── insert_to_db.py
│
├── tests/
│   ├── test_agents.py
│   └── test_api.py
│
├── streamlit_app.py
├── requirements.txt
├── README.md
├── docker-compose.yml
├── .env
└── .gitignore
