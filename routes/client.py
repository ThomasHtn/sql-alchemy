import os

import joblib
import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from models import ClientProfile
from schemas import ClientCreate, ClientInput, ClientUpdate
from utils.base import SessionLocal
from utils.database_management import create_client

router = APIRouter(prefix="/clients", tags=["clients"])

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load model and preprocessor
model = joblib.load(os.path.join(BASE_DIR, "model_artifacts", "model2.pkl"))
preprocessor = joblib.load(
    os.path.join(BASE_DIR, "model_artifacts", "preprocessor2.pkl")
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =============================
# GET: All clients
# =============================
@router.get("/", summary="Get all clients")
def read_clients(db: Session = Depends(get_db)):
    return db.query(ClientProfile).all()


# =============================
# POST: Add client
# =============================
@router.post("/", summary="Add a new client")
def add_client(client: ClientCreate, db: Session = Depends(get_db)):
    print("POST: add client route called")

    return create_client(db, client)


# =============================
# GET: Get client by id
# =============================
@router.get("/{client_id}", summary="Get client by ID")
def get_client(client_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    print("GET: client route called")

    # Get client by id in database
    client = db.query(ClientProfile).filter(ClientProfile.id == client_id).first()

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    return client


# =============================
# PATCH: Patch client by id
# =============================
@router.patch("/{client_id}", summary="Partially update a client")
def partial_update_client(
    client_id: int, updated_fields: ClientUpdate, db: Session = Depends(get_db)
):
    print("PATCH: client route called")

    # Get client by id in database
    client = db.query(ClientProfile).filter(ClientProfile.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    # Update each value in updated_fields
    for field, value in updated_fields.model_dump(exclude_unset=True).items():
        setattr(client, field, value)

    db.commit()
    db.refresh(client)

    return client


# =============================
# DELETE: Delete client by id
# =============================
@router.delete("/{client_id}", summary="Delete client by ID")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    print("DELETE: client route called")

    # Get client by id in database
    client = db.query(ClientProfile).filter(ClientProfile.id == client_id).first()

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    db.delete(client)
    db.commit()

    return {"message": f"Client with ID {client_id} deleted"}


# =============================
# POST: Predict loan value
# =============================
@router.post("/predict", summary="Predict value")
def predict(client: ClientInput, db: Session = Depends(get_db)):
    input_dict = {
        "age": [client.age],
        "taille": [client.height_cm],
        "poids": [client.weight_kg],
        "sport_licence": [client.has_sports_license],
        "niveau_etude": [client.education_level],
        "region": [client.region],
        "smoker": [client.is_smoker],
        "revenu_estime_mois": [client.estimated_monthly_income],
        "situation_familiale": [client.marital_status],
        "historique_credits": [client.credit_history],
        "risque_personnel": [client.personal_risk_score],
        "score_credit": [client.credit_score],
        "loyer_mensuel": [client.monthly_rent],
        "nb_enfants": [client.nb_enfants],
        "quotient_caf": [client.quotient_caf],
    }

    try:
        df = pd.DataFrame(input_dict)

        # Prétraitement
        X_processed = preprocessor.transform(df)

        # Prédiction avec le modèle Keras
        prediction = model.predict(X_processed)

        return {"predicted_loan_amount": float(prediction[0][0])}

    except Exception as e:
        return {"error": "Prediction failed", "detail": str(e)}
