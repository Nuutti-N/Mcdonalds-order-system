
from sqlmodel import SQLModel, create_engine
import os
from dotenv import load_dotenv
load_dotenv()

engine = create_engine(os.getenv("DataBase_URL"))
SQLModel.metadata.create_all(engine)
