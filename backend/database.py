import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session
from models import Task, Conversation, Message

# .env file load karne ke liye:
load_dotenv() 

DATABASE_URL = os.getenv("DATABASE_URL")

# Check karein agar URL None hai toh error show kare
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in .env file")

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session