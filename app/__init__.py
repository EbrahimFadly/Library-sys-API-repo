import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()
db = create_engine(os.getenv("sqlite_url"))
