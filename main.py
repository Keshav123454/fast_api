from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, init_db
import models, schemas, crud, utils
from typing import List

init_db()

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/accounts/", response_model=schemas.Account)
def create_account(account: schemas.AccountCreate, db: Session = Depends(get_db)):
    db_account = crud.get_account_by_email(db, email=account.email)
    if db_account:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_account(db=db, account=account)

@app.get("/accounts/{account_id}", response_model=schemas.Account)
def read_account(account_id: int, db: Session = Depends(get_db)):
    db_account = crud.get_account(db, account_id=account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account

@app.post("/destinations/{account_id}", response_model=schemas.Destination)
def create_destination_for_account(account_id: int, destination: schemas.DestinationCreate, db: Session = Depends(get_db)):
    return crud.create_destination(db=db, destination=destination, account_id=account_id)

@app.post("/server/incoming_data")
def receive_data(data: dict, cl_x_token: str, db: Session = Depends(get_db)):
    account = db.query(models.Account).filter(models.Account.app_secret_token == cl_x_token).first()
    if not account:
        return {"detail": "Un Authenticate"}
    destinations = account.destinations
    for destination in destinations:
        utils.send_data(destination, data)
    return {"status": "success"}

@app.get("/destinations/{account_id}", response_model=List[schemas.Destination])
def get_destinations_for_account(account_id: int, db: Session = Depends(get_db)):
    account = crud.get_account(db, account_id=account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return account.destinations

