from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from starlette.middleware.sessions import SessionMiddleware

from .routers import general, users, auth, places
from . import models
from .settings import Settings
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
settings = Settings()

app.mount('/static', StaticFiles(directory="app/static"), name="static")

app.include_router(places.router)
app.include_router(auth.router)
app.include_router(general.router)
app.include_router(users.router)

SECRET_KEY = settings.secret_key
if SECRET_KEY is None:
    raise 'Missing SECRET_KEY'
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
