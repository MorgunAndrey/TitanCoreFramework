# config/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Environment variable {name} must be set")
    return value

database_user = _require_env("database_user")
database_password = _require_env("database_password")
database_host = _require_env("database_host")
database_port = _require_env("database_port")
database_name = _require_env("database_name")

if database_user == "root" and not database_password:
    raise RuntimeError("Database password must not be empty for user 'root'")

DATABASE_URL = f"mysql+pymysql://{database_user}:{database_password}@{database_host}:{database_port}/{database_name}"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()