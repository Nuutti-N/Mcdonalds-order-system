
from sqlmodel import SQLModel, create_engine
import os
from dotenv import load_dotenv
load_dotenv()

engine = create_engine(os.getenv("database_url"))
SQLModel.metadata.create_all(engine)
