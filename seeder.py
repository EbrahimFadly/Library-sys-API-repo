from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.models import Base, User, Reader, Book
from passlib.hash import bcrypt
import os
from dotenv import load_dotenv


# Sample data
sample_librarians = [
    User(email="admin1@example.com", password=bcrypt.hash("password123")),
    User(email="admin2@example.com", password=bcrypt.hash("pass1234")),
]

sample_readers = [
    Reader(name="Alice Smith", email="alice@example.com"),
    Reader(name="Bob Jones", email="bob@example.com"),
]

sample_books = [
    Book(
        title="The Psychology of Prejudice: From Attitudes to Social Action",
        author="Lynne M. Jackson",
        year=2019,
        isbn="1234567890",
        copies_available=3,
    ),
    Book(
        title="Brave New World",
        author="Aldous Huxley",
        year=1932,
        isbn="0987654321",
        copies_available=0,
    ),
]


def seed_data_sqlite():
    load_dotenv()
    engine = create_engine(os.getenv("sqlite_url"))
    LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    db = LocalSession()
    # Create all tables
    Base.metadata.create_all(bind=engine)
    try:
        # Clear old data
        # db.query(Book).delete()
        # db.query(Reader).delete()
        # db.query(Librarian).delete()
        # db.commit()

        # Add new data
        db.add_all(sample_librarians)
        db.add_all(sample_readers)
        db.add_all(sample_books)
        db.commit()
        print("data inserted successfully.")
    finally:
        db.close()


def seed_data_postgres():

    load_dotenv()
    postgres_url = (
        f"postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_DATABASE')}"
    )

    engine = create_engine(postgres_url)
    LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    db = LocalSession()

    # Create all tables
    Base.metadata.create_all(bind=engine)
    try:
        # Add new data
        db.add_all(sample_librarians)
        db.add_all(sample_readers)
        db.add_all(sample_books)
        db.commit()
        print("data inserted successfully.")
    finally:
        db.close()


if __name__ == "__main__":
    # seed_data_sqlite()
    seed_data_postgres()
