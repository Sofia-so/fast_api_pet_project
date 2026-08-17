from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

from app.config import settings

load_dotenv()
DATABASE_URI = os.getenv("DATABASE_URI")
engine = create_engine(settings.database_uri)
# engine = create_engine(
#     DATABASE_URI,
#     echo=True
# )
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False)

TEST_DATABASE_URI = os.getenv("TEST_DATABASE_URI")
test_engine = create_engine(settings.test_database_uri)
# test_engine = create_engine(
#     TEST_DATABASE_URI,
#     echo=True
# )
TestSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False
)
