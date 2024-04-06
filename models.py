from database import Base
from sqlalchemy import Column, Integer, String

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Integer)

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String,unique=True)
    firstName = Column(String)
    lastName = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)
