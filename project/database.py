
from sqlmodel import SQLModel, create_engine
import os
from dotenv import load_dotenv
load_dotenv()

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise ValueError("check your .env file")
engine = create_engine(database_url)
SQLModel.metadata.create_all(engine)
