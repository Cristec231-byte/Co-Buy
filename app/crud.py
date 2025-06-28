from sqlalchemy.orm import Session

import schemas
import models

# Item CRUD operations
def get_items(db: Session):
    return db.query(models.Item).all()

def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()

def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(**item.model_dump())  # Updated for Pydantic v2
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, item_id: int, item: schemas.ItemCreate):
    db_item = get_item(db, item_id)
    if db_item:
        db_item.name = item.name
        db_item.description = item.description
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int):
    db_item = get_item(db, item_id)
    if db_item:
        db.delete(db_item)
        db.commit()
    return {"deleted": True}

# Data CRUD operations for testing PostgreSQL
def get_data_entries(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Data).offset(skip).limit(limit).all()

def get_data_entry(db: Session, data_id: int):
    return db.query(models.Data).filter(models.Data.id == data_id).first()

def create_data_entry(db: Session, data: schemas.DataCreate):
    db_data = models.Data(**data.model_dump())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

def update_data_entry(db: Session, data_id: int, data: schemas.DataUpdate):
    db_data = get_data_entry(db, data_id)
    if db_data:
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_data, field, value)
        db.commit()
        db.refresh(db_data)
    return db_data

def delete_data_entry(db: Session, data_id: int):
    db_data = get_data_entry(db, data_id)
    if db_data:
        db.delete(db_data)
        db.commit()
        return {"deleted": True}
    return {"deleted": False, "message": "Data entry not found"}
