from sqlalchemy.orm import Session
from sqlalchemy import func
import models, schemas

# CRUD operations for Test table
def create_test_item(db: Session, test_item: schemas.TestTableCreate):
    db_item = models.TestTable(**test_item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_test_item(db: Session, item_id: int):
    return db.query(models.TestTable).filter(models.TestTable.id == item_id).first()

def get_test_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.TestTable).offset(skip).limit(limit).all()

def update_test_item(db: Session, item_id: int, test_item: schemas.TestTableUpdate):
    db_item = db.query(models.TestTable).filter(models.TestTable.id == item_id).first()
    if db_item:
        for key, value in test_item.dict(exclude_unset=True).items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_test_item(db: Session, item_id: int):
    db_item = db.query(models.TestTable).filter(models.TestTable.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item
