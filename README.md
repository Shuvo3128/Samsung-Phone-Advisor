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










