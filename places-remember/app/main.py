from fastapi import FastAPI
from routers import general, users, auth
from starlette.middleware.sessions import SessionMiddleware
import models
from settings import Settings
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
settings = Settings()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.include_router(auth.router)
app.include_router(general.router)
app.include_router(users.router)

SECRET_KEY = settings.secret_key
if SECRET_KEY is None:
    raise 'Missing SECRET_KEY'
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
