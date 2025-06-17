import pandas as pd
from fastapi import FastAPI

from crud.client import populateTableFromCSV, show_values
from database import SessionLocal, create_tables
from models.client import ClientProfile
from routes import client

app = FastAPI()


# Register routes
app.include_router(client.router)

# Create tables if needed
create_tables()

results = SessionLocal().query(ClientProfile).all()
if len(results) == 0:
    print("no data... populate database from csv")

    # Load csv
    df = pd.read_csv("data/data.csv")

    # Populate database from csv
    populateTableFromCSV(SessionLocal(), df)
else:
    print("Already populate")

show_values(SessionLocal())
