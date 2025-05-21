import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker


load_dotenv()
db = create_engine(os.getenv("sqlite_url"))
Base = declarative_base()


LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=db)
