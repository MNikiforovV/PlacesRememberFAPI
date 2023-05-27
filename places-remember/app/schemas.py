from pydantic import BaseModel


class Place(BaseModel):
    title: str
    description: str

    latitude: float
    longitude: float

    author_id: int

    class Config:
        orm_mode = True


class User(BaseModel):
    email: str
    first_name: str
    last_name: str
    profile_picture_url: str

    places: list[Place] = []

    class Config:
        orm_mode = True
