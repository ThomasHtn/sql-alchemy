from sqlalchemy.orm import Session

from models.client import ClientProfile
from schemas.client import ClientCreate


def create_client(db: Session, client: ClientCreate):
    db_client = ClientProfile(**client.model_dump())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


def show_values(db: Session):
    results = db.query(ClientProfile).all()

    if len(results) == 0:
        print("no data.")
    else:
        for item in results:
            print(
                f"{item.firstname} {item.lastname}, Age: {item.age}, Score: {item.credit_score}, Income: €{item.estimated_monthly_income}, Children: {item.nb_enfants},"
            )


def populateTableFromCSV(db: Session, df):
    for _, row in df.iterrows():
        new_client = ClientProfile(
            lastname=row["nom"],
            firstname=row["prenom"],
            age=row["age"],
            height_cm=row["taille"],
            weight_kg=row["poids"],
            gender=row["sexe"],
            has_sports_license=bool(row["sport_licence"]),
            education_level=row["niveau_etude"],
            region=row["region"],
            is_smoker=bool(row["smoker"]),
            is_french_national=bool(row["nationalité_francaise"]),
            estimated_monthly_income=row["revenu_estime_mois"],
            marital_status=row["situation_familiale"],
            credit_history=row["historique_credits"],
            personal_risk_score=row["risque_personnel"],
            credit_score=row["score_credit"],
            monthly_rent=row["loyer_mensuel"],
            loan_amount_requested=row["montant_pret"],
        )
        db.add(new_client)
        db.commit()
