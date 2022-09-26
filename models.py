from sqlalchemy import Column, Integer, String, Float
from database import Base

class vietnamese_gender_prediction(Base):
    __tablename__ = "vietnamese gender prediction"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    gender = Column(String)
    accuracy = Column(Float)



