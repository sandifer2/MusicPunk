from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from app.core.config import get_settings
import os

load_dotenv()

settings = get_settings()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD  = os.getenv("DB_PASSWORD")

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(
    DB_URL,
    echo=settings.DEBUG if hasattr(settings,'DEBUG') else False, #log sql if in debug 
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True, #check for dead connection
    pool_recycle=3600, #prevent stale connections

    connect_args={
        "connect_timeout": 10,
        "application_name": "musicbox_api"
    }
)

SessionLocal = sessionmaker( #session obj for db to use, manually flush or commit
    autocommit=False,  
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    '''Creates db tables if they dont exist'''
    Base.metadata.create_all(bind=engine)

def test_connection():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            if result:
                print("Connection success.")
                return True
            else:
                raise RuntimeError("Result holding select 1 statement does not exist.")
    except Exception as e:
        print(f"Error: Connection Unsuccessful: {e}")
        return False



