import pandas as pd
from sqlalchemy.orm import Session

from database import SessionLocal
from models.client import ClientProfile


def update_database():
    print("triger updated")

    # Load the new CSV
    df = pd.read_csv("./data/fresh-data.csv")

    print(df.info)

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
