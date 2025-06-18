from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from database import SessionLocal
from models.client import ClientProfile
from schemas.client import ClientCreate, ClientUpdate
from utils.database_management import create_client

router = APIRouter(prefix="/clients", tags=["clients"])


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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

    client = db.query(ClientProfile).filter(ClientProfile.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

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

    client = db.query(ClientProfile).filter(ClientProfile.id == client_id).first()

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    db.delete(client)
    db.commit()

    return {"message": f"Client with ID {client_id} deleted"}
