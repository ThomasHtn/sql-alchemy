from fastapi import FastAPI
from sqlalchemy import func

from models.client import ClientProfile
from module import simple_model_train
from routes import client
from utils.database_management import (
    SessionLocal,
    create_tables,
    populate_from_csv,
    show_last_rows,
)

app = FastAPI()


# Register routes
app.include_router(client.router)


# ==================================================
# 01 :
# Train model without (nb_enfant, quotien_caf)
# Use a clean data set
# ==================================================

simple_model_train()

# ==================================================
# 02 :
# Load dataset into database
# ==================================================

# Create tables if needed
create_tables()

# Populate database if needed
count = SessionLocal().query(func.count(ClientProfile.id)).scalar()

if count == 0:
    populate_from_csv(SessionLocal(), "clean-data.csv")
    show_last_rows(SessionLocal(), 10)
    new_count = SessionLocal().query(func.count(ClientProfile.id)).scalar()
    print(f"Row in table : {new_count}")
else:
    print(f"Current row in table : {count}")


# ==================================================
# 03 :
# Retrain existing model
# Use data from database
# Retrain model with (nb_enfant, quotien_caf)
# ==================================================
