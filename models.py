from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from database import Base

class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    app_secret_token = Column(String, unique=True, index=True)
    website = Column(String, nullable=True)
    destinations = relationship("Destination", back_populates="owner")

class Destination(Base):
    __tablename__ = "destinations"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    http_method = Column(String, nullable=False)
    headers = Column(JSON, nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    owner = relationship("Account", back_populates="destinations")

