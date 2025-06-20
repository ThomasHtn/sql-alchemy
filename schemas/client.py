from typing import Optional

from pydantic import BaseModel


# =============================
# CREATE: Create client schema
# =============================
class ClientCreate(BaseModel):
    age: int
    height_cm: float
    weight_kg: float
    has_sports_license: bool
    education_level: int
    region: str
    is_smoker: bool
    estimated_monthly_income: float
    marital_status: str
    credit_history: str
    personal_risk_score: float
    credit_score: int
    monthly_rent: float
    loan_amount_requested: float
    nb_enfants: Optional[int] = None
    quotient_caf: Optional[float] = None


# =============================
# UPDATE: update client schema
# =============================
class ClientUpdate(BaseModel):
    age: Optional[int] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    has_sports_license: Optional[bool] = None
    education_level: Optional[str] = None
    region: Optional[str] = None
    is_smoker: Optional[bool] = None
    estimated_monthly_income: Optional[float] = None
    marital_status: Optional[str] = None
    credit_history: Optional[str] = None
    personal_risk_score: Optional[float] = None
    credit_score: Optional[int] = None
    monthly_rent: Optional[float] = None
    loan_amount_requested: Optional[float] = None
    nb_enfants: Optional[int] = None
    quotient_caf: Optional[float] = None

    class Config:
        from_attributes = True
