import pandas as pd
from fastapi import FastAPI

from database import SessionLocal, create_tables
from models.client import ClientProfile
from routes import client
from utils.database_management import populateDatabaseFromCSV, update_database

app = FastAPI()


# Register routes
app.include_router(client.router)

# Create tables if needed
create_tables()

# Populate database with first CSV if needed
results = SessionLocal().query(ClientProfile).all()
if len(results) == 0:
    print("no data... populate database from csv")

    # Load csv
    df = pd.read_csv("data/data.csv")

    # Populate database from csv
    populateDatabaseFromCSV(SessionLocal(), df)
else:
    print("Already populate")


# Populate databese with new columns from new CSV if needed
clients_with_children = (
    SessionLocal()
    .query(ClientProfile)
    .filter(ClientProfile.nb_enfants.isnot(None))
    .all()
)
if len(clients_with_children) == 0:
    update_database()
else:
    print("alredy updated")
