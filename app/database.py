import os
import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import *

DATABASE_URL = os.getenv("DATABASE_URL")

engine = None

for attempt in range(10):
    try:
        engine = create_engine(DATABASE_URL)
        connection = engine.connect()
        connection.close()
        print("Database connected successfully.")
        break
    except Exception as e:
        print(f"Database not ready, retrying... ({attempt+1}/10)")
        time.sleep(3)
        
if engine is None:
    raise Exception("Could not connect to database after multiple attempts.")

sessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()