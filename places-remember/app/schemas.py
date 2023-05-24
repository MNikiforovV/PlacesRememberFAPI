from pydantic import BaseModel


class User(BaseModel):
    email: str
    first_name: str
    last_name: str
    profile_picture_url: str

    class Config:
        orm_mode = True
