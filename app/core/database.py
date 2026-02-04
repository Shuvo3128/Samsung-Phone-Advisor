from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.settings import settings

DATABASE_URL = (
    f"postgresql+psycopg2://{settings.DB_USER}:"
    f"{settings.DB_PASSWORD}@"
    f"{settings.DB_HOST}:"
    f"{settings.DB_PORT}/"
    f"{settings.DB_NAME}"
)


# SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    echo=True,   # show SQL logs (development only)
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base class for models
Base = declarative_base()


# FastAPI dependency (DB session per request)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
