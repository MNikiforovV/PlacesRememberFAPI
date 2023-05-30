from sqlalchemy.orm import Session

from ..models import User as UserModel
from ..schemas import User as UserSchema


# Method returns user by email from database.
def get_user_by_email(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email).first()


# Method creates user in database with pydantic user schema.
def create_user(db: Session, user: UserSchema):
    db_user = UserModel()
    db_user.email = user.email
    db_user.first_name = user.first_name
    db_user.last_name = user.last_name
    db_user.profile_picture_url = user.profile_picture_url
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
