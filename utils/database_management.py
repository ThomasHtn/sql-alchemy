from os.path import join as join
from pathlib import Path

import pandas as pd
from sqlalchemy.orm import Session

from models import ClientProfile
from schemas import ClientCreate
from utils import BOOL_MAP, CSV_TO_DB_MAP, EDUCATION_MAP
from utils.base import Base, engine


# ===================================
# Create all sqlAlchemy table
# ===================================
def create_tables():
    Base.metadata.create_all(bind=engine)


# ===================================
# Populate database from a given CSV
# ===================================
def populate_from_csv(session: Session, csv_path: str):
    # Get "data" root dir
    root_dir = Path(__file__).resolve().parent.parent
    data_path = root_dir / "data" / csv_path

    # read csv
    df = pd.read_csv(data_path)

    # Iterate on each csv row
    for _, row in df.iterrows():
        data = {}

        for csv_col, db_field in CSV_TO_DB_MAP.items():
            value = row.get(csv_col, None)

            # Specific column management
            if db_field in ["has_sports_license", "is_smoker"]:
                data[db_field] = BOOL_MAP.get(str(value).strip().lower(), None)

            elif db_field == "education_level":
                data[db_field] = EDUCATION_MAP.get(str(value).strip().lower(), None)

            elif pd.isna(value):
                data[db_field] = None

            else:
                data[db_field] = value

        # Init SqlAlchemy object
        client = ClientProfile(**data)

        session.add(client)

    session.commit()


# ===================================
# Add a new client in database
# ===================================
def create_client(db: Session, client: ClientCreate):
    db_client = ClientProfile(**client.model_dump())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


# ===================================
# Display last X rows from database
# ===================================
def show_last_rows(db: Session, limit: 10):
    results = (
        db.query(ClientProfile).order_by(ClientProfile.id.desc()).limit(limit).all()
    )

    if len(results) == 0:
        print("no data.")
    else:
        for item in results:
            print(
                f"ID: {item.id}, Age: {item.age}, Score: {item.credit_score}, Income: €{item.estimated_monthly_income}, Children: {item.nb_enfants},"
            )
