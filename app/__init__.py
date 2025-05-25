import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI


load_dotenv()

# postgres_url = (
#     f"postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@"
#     f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_DATABASE')}"
# )
sqlite_url = os.getenv("sqlite_url")
db = create_engine(sqlite_url, echo=True)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db)


def LocalSession():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def createApp():
    app = FastAPI()

    from .auth import router as auth_router
    from .BookManagment import router as book_router
    from .reader_manager import router as reader_router

    app.include_router(auth_router)
    app.include_router(book_router)
    app.include_router(reader_router)

    return app
