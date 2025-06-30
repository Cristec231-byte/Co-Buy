from sqlalchemy.orm import Session
from sqlalchemy import func
import models, schemas

# Item CRUD operations
def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()

def update_item(db: Session, item_id: int, item: schemas.ItemCreate):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item:
        update_data = item.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_item, field, value)
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return {"message": "Item deleted successfully"}

# Investor CRUD operations
def create_investor(db: Session, investor: schemas.InvestorCreate):
    db_investor = models.Investor(**investor.model_dump())
    db.add(db_investor)
    db.commit()
    db.refresh(db_investor)
    return db_investor

def get_investors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Investor).offset(skip).limit(limit).all()

def get_investor(db: Session, investor_id: int):
    return db.query(models.Investor).filter(models.Investor.id == investor_id).first()

def get_investor_by_email(db: Session, email: str):
    return db.query(models.Investor).filter(models.Investor.email == email).first()

def update_investor(db: Session, investor_id: int, investor: schemas.InvestorUpdate):
    db_investor = db.query(models.Investor).filter(models.Investor.id == investor_id).first()
    if db_investor:
        update_data = investor.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_investor, field, value)
        # last_updated will be automatically updated by the database
        db.commit()
        db.refresh(db_investor)
    return db_investor

def delete_investor(db: Session, investor_id: int):
    db_investor = db.query(models.Investor).filter(models.Investor.id == investor_id).first()
    if db_investor:
        db.delete(db_investor)
        db.commit()
    return {"message": "Investor deleted successfully"}

def search_investors(db: Session, search_term: str, skip: int = 0, limit: int = 100):
    """Search investors by name or email"""
    return db.query(models.Investor).filter(
        (models.Investor.first_name.ilike(f"%{search_term}%")) |
        (models.Investor.last_name.ilike(f"%{search_term}%")) |
        (models.Investor.email.ilike(f"%{search_term}%"))
    ).offset(skip).limit(limit).all()

# Journal CRUD operations (updated for journal_number as primary key)
def create_journal(db: Session, journal: schemas.JournalCreate):
    db_journal = models.Journal(**journal.model_dump())
    db.add(db_journal)
    db.commit()
    db.refresh(db_journal)
    return db_journal

def get_journals(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Journal).offset(skip).limit(limit).all()

def get_journal(db: Session, journal_number: str):
    return db.query(models.Journal).filter(models.Journal.journal_number == journal_number).first()

def update_journal(db: Session, journal_number: str, journal: schemas.JournalUpdate):
    db_journal = db.query(models.Journal).filter(models.Journal.journal_number == journal_number).first()
    if db_journal:
        update_data = journal.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_journal, field, value)
        # updated timestamp will be automatically updated by the database
        db.commit()
        db.refresh(db_journal)
    return db_journal

def delete_journal(db: Session, journal_number: str):
    db_journal = db.query(models.Journal).filter(models.Journal.journal_number == journal_number).first()
    if db_journal:
        db.delete(db_journal)
        db.commit()
    return {"message": "Journal deleted successfully"}

def search_journals(db: Session, search_term: str, skip: int = 0, limit: int = 100):
    """Search journals by journal number or file type"""
    return db.query(models.Journal).filter(
        (models.Journal.journal_number.ilike(f"%{search_term}%")) |
        (models.Journal.file_type.ilike(f"%{search_term}%"))
    ).offset(skip).limit(limit).all()

def update_journal_last_loaded(db: Session, journal_number: str):
    """Update the last_loaded timestamp to current time"""
    db_journal = db.query(models.Journal).filter(models.Journal.journal_number == journal_number).first()
    if db_journal:
        db_journal.last_loaded = func.now()
        db.commit()
        db.refresh(db_journal)
    return db_journal
