from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import Base


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@postgres/postgres"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


tables_created = False

def create_tables():
    global tables_created
    if not tables_created:
        Base.metadata.create_all(engine)
        tables_created = True