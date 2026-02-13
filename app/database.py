from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager

DATABASE_URL = "postgresql://postgres:admin123@localhost:5432/backend_db"

engine = create_engine(DATABASE_URL)

sessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()