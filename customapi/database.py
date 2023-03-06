from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from sqlalchemy.util.compat import contextmanager

DATABASE_URL = "postgresql://postgres:catgptdb@postgres.catgpt.fun:5432/postgres"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


def get_db() -> Optional[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


session = contextmanager(get_db)