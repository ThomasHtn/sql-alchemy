from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Replace by "sqlite:///:memory:" to use in-memory database 
engine = create_engine("sqlite:///./data/generated-client.db")
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


def create_tables():
    Base.metadata.create_all(bind=engine)
