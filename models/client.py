from sqlalchemy import Boolean, Column, Float, Integer, String

from database import Base


class ClientProfile(Base):
    __tablename__ = "client_profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    lastname = Column(String(100), nullable=True)
    firstname = Column(String(100), nullable=True)
    age = Column(Integer, nullable=True)
    height_cm = Column(Float, nullable=True)
    weight_kg = Column(Float, nullable=True)
    gender = Column(String(10), nullable=True)
    has_sports_license = Column(Boolean, nullable=True)
    education_level = Column(String(100), nullable=True)
    region = Column(String(100), nullable=True)
    is_smoker = Column(Boolean, nullable=True)
    is_french_national = Column(Boolean, nullable=True)
    estimated_monthly_income = Column(Float, nullable=True)
    marital_status = Column(String(50), nullable=True)
    credit_history = Column(String(500), nullable=True)
    personal_risk_score = Column(Float, nullable=True)
    credit_score = Column(Integer, nullable=True)
    monthly_rent = Column(Float, nullable=True)
    loan_amount_requested = Column(Float, nullable=True)
