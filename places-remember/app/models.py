from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    profile_picture_url = Column(String)

    places = relationship("Place", back_populates="author")


class Place(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)

    latitude = Column(Float)
    longitude = Column(Float)

    author_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("User", back_populates="places")
