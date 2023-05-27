from sqlalchemy.orm import Session

from ..models import Place as PlaceModel
from ..schemas import Place as PlaceSchema


def get_places_by_user(db: Session, user_id: int):
    return db.query(PlaceModel).filter(PlaceModel.author_id == user_id).all()


def get_place_by_id(db: Session, place_id: int):
    return db.query(PlaceModel).filter(PlaceModel.id == place_id).first()


def create_place(db: Session, place: PlaceSchema):
    db_place = PlaceModel(**place.dict())
    db.add(db_place)
    db.commit()
    db.refresh(db_place)
    return db_place


def edit_place(db: Session, place: PlaceSchema, place_id: int):
    # place_to_edit = get_place_by_id(db=db, place_id=place.id)
    pass
