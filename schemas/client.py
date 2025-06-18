from typing import Optional

from pydantic import BaseModel


class ClientCreate(BaseModel):
    lastname: str
    firstname: str
    age: int
    height_cm: float
    weight_kg: float
    gender: str
    has_sports_license: bool
    education_level: str
    region: str
    is_smoker: bool
    is_french_national: bool
    estimated_monthly_income: float
    marital_status: str
    credit_history: str
    personal_risk_score: float
    credit_score: int
    monthly_rent: float
    loan_amount_requested: float
    orientation_sexuelle: Optional[str] = None
    nb_enfants: Optional[int] = None
    quotient_caf: Optional[float] = None


class ClientUpdate(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    age: Optional[int] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    gender: Optional[str] = None
    has_sports_license: Optional[bool] = None
    education_level: Optional[str] = None
    region: Optional[str] = None
    is_smoker: Optional[bool] = None
    is_french_national: Optional[bool] = None
    estimated_monthly_income: Optional[float] = None
    marital_status: Optional[str] = None
    credit_history: Optional[str] = None
    personal_risk_score: Optional[float] = None
    credit_score: Optional[int] = None
    monthly_rent: Optional[float] = None
    loan_amount_requested: Optional[float] = None
    orientation_sexuelle: Optional[str] = None
    nb_enfants: Optional[int] = None
    quotient_caf: Optional[float] = None

    class Config:
        from_attributes = True  # Pydantic v2
