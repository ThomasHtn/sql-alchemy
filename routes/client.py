from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from crud.client import create_client
from database import SessionLocal
from models.client import ClientProfile
from schemas.client import ClientCreate, ClientUpdate

router = APIRouter(prefix="/clients", tags=["clients"])


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Add client
@router.post("/", summary="Add a new client")
def add_client(client: ClientCreate, db: Session = Depends(get_db)):
    print("POST: client")
    return create_client(db, client)


# Get client
@router.get("/{client_id}", summary="Get client by ID")
def get_client(client_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    print("GET: client")

    client = db.query(ClientProfile).filter(ClientProfile.id == client_id).first()

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    return client


# Patch client
@router.patch("/{client_id}", summary="Partially update a client")
def partial_update_client(
    client_id: int, updated_fields: ClientUpdate, db: Session = Depends(get_db)
):
    print("PATCH: client")

    client = db.query(ClientProfile).filter(ClientProfile.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    for field, value in updated_fields.model_dump(exclude_unset=True).items():
        setattr(client, field, value)

    db.commit()
    db.refresh(client)
    return client


# Delete client
@router.delete("/{client_id}", summary="Delete client by ID")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    print("DELETE: client")

    client = db.query(ClientProfile).filter(ClientProfile.id == client_id).first()

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    db.delete(client)
    db.commit()

    return {"message": f"Client with ID {client_id} deleted"}
