import pandas as pd
from sqlalchemy.orm import Session

from database import SessionLocal
from models.client import ClientProfile
from schemas.client import ClientCreate


def populateDatabaseFromCSV(db: Session, df):
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


def update_database():
    print("triger updated")

    # Load the new CSV
    df = pd.read_csv("./data/fresh-data.csv")

    # Start DB session
    db: Session = SessionLocal()

    for _, row in df.iterrows():
        # Identify the client (adjust matching logic as needed)
        client = (
            db.query(ClientProfile)
            .filter(
                ClientProfile.firstname == row["prenom"],
                ClientProfile.lastname == row["nom"],
            )
            .first()
        )

        if client:
            updated = False

            # Update only if current value is None
            if client.nb_enfants is None and pd.notna(row.get("nb_enfants")):
                client.nb_enfants = row["nb_enfants"]
                updated = True

            if client.quotient_caf is None and pd.notna(row.get("quotient_caf")):
                client.quotient_caf = row["quotient_caf"]
                updated = True

            if client.orientation_sexuelle is None and pd.notna(
                row.get("orientation_sexuelle")
            ):
                client.orientation_sexuelle = row["orientation_sexuelle"]
                updated = True

            if updated:
                db.commit()
                print(f"✅ Updated: {client.firstname} {client.lastname}")
            else:
                print(f"⏩ No update needed: {client.firstname} {client.lastname}")
        else:
            print(f"⚠️  Client not found: {row['firstname']} {row['lastname']}")

    db.close()


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
