from sqlalchemy.orm import Session
from ModelAI_LSTM.utils import test_model
import models


def get_name_by_id(db: Session, name_id: int):
    return db.query(models.vietnamese_gender_prediction).filter(models.vietnamese_gender_prediction.id == name_id).first()


def get_name_by_name(db: Session, name: str):
    return db.query(models.vietnamese_gender_prediction).filter(models.vietnamese_gender_prediction.name == name).first()


def get_names(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.vietnamese_gender_prediction).offset(skip).limit(limit).all()
# Create result function for adding data in table
##predict_names function for supporting the create_result dunction
def predict_names(names: set[str]):
    if names:
        results = test_model(names)
        return results
    else:
        return None
def create_result(db: Session, results: list):
    if results:
        for result in results:
            db_name = models.vietnamese_gender_prediction(name=result[0], gender=result[1], accuracy=round(result[2], 2))
            db.add(db_name)
            db.commit()
            db.refresh(db_name)
    return db.query(models.vietnamese_gender_prediction).all()
#

