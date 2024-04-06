from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker

DATABASE_URL = "sqlite:///./products.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine,autocommit=False)
Base = declarative_base()