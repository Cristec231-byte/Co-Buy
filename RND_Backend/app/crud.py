from sqlalchemy.orm import Session
from sqlalchemy import func
import models, schemas

# CRUD operations for Data table
def create_data_item(db: Session, data_item: schemas.DataCreate):
    db_item = models.Data()
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_data_item(db: Session, item_id: int):
    return db.query(models.Data).filter(models.Data.id == item_id).first()

def get_data_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Data).offset(skip).limit(limit).all()

def delete_data_item(db: Session, item_id: int):
    db_item = db.query(models.Data).filter(models.Data.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item

