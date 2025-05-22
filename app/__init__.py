import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker


load_dotenv()

# postgres_url = (
#         f"postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@"
#         f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_DATABASE')}"
#     )
sqlite_url = os.getenv("sqlite_url")
db = create_engine(sqlite_url)
Base = declarative_base()


LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=db)
