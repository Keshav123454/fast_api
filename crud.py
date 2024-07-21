from sqlalchemy.orm import Session
import models, schemas

def get_account(db: Session, account_id: int):
    return db.query(models.Account).filter(models.Account.id == account_id).first()

def get_account_by_email(db: Session, email: str):
    return db.query(models.Account).filter(models.Account.email == email).first()

def get_accounts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Account).offset(skip).limit(limit).all()

def create_account(db: Session, account: schemas.AccountCreate):
    db_account = models.Account(email=account.email, name=account.name, app_secret_token="your_secret_token", website=account.website)
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

def get_destination(db: Session, destination_id: int):
    return db.query(models.Destination).filter(models.Destination.id == destination_id).first()

def create_destination(db: Session, destination: schemas.DestinationCreate, account_id: int):
    db_destination = models.Destination(**destination.dict(), account_id=account_id)
    db.add(db_destination)
    db.commit()
    db.refresh(db_destination)
    return db_destination

