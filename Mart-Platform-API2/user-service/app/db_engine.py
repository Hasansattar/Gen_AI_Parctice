# app/db_engine.py
from sqlmodel import SQLModel, create_engine
from app  import settings
import time
from sqlalchemy.exc import OperationalError


connection_string = str(settings.DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)


engine = create_engine(
    connection_string, connect_args={}, pool_recycle=300
)


def create_db_and_tables() -> None:
    # SQLModel.metadata.create_all(engine)
    max_retries = 5
    retry_wait = 5  # seconds

    for attempt in range(max_retries):
        try:
            SQLModel.metadata.create_all(engine)
            print("Database connected and tables created.")
            break
        except OperationalError as e:
            print(f"Database connection failed. Attempt {attempt + 1} of {max_retries}. Retrying in {retry_wait} seconds...")
            time.sleep(retry_wait)
    else:
        print("Could not connect to the database after several attempts.")



