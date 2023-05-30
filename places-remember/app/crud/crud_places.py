from sqlalchemy.orm import Session

from ..models import Place as PlaceModel
from ..schemas import Place as PlaceSchema


# Method returns all saved user's places by user id from database.
def get_places_by_user(db: Session, user_id: int):
    return db.query(PlaceModel).filter(PlaceModel.author_id == user_id).all()


# Method returns one place by its id from database.
def get_place_by_id(db: Session, place_id: int):
    return db.query(PlaceModel).filter(PlaceModel.id == place_id).first()


# Method creates new place in database with pydantic place schema.
def create_place(db: Session, place: PlaceSchema):
    db_place = PlaceModel(**place.dict())
    db.add(db_place)
    db.commit()
    db.refresh(db_place)
    return db_place
