from fastapi import Depends, APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.encoders import jsonable_encoder
from starlette.config import Config
from authlib.integrations.starlette_client import OAuth, OAuthError
from settings import Settings

from sqlalchemy.orm import Session

from crud.crud_user import get_user_by_email, create_user
from dependencies import get_db
from schemas import User

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)
settings = Settings()

GOOGLE_CLIENT_ID = settings.google_client_id
GOOGLE_CLIENT_SECRET = settings.google_client_secret
if GOOGLE_CLIENT_ID is None or GOOGLE_CLIENT_SECRET is None:
    raise BaseException('Missing env variables')

config_data = {
    'GOOGLE_CLIENT_ID': GOOGLE_CLIENT_ID,
    'GOOGLE_CLIENT_SECRET': GOOGLE_CLIENT_SECRET
    }
config = Config(environ=config_data)
oauth = OAuth(config)

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)


@router.get('/login')
async def login(request: Request):
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, str(redirect_uri))


@router.get('/auth')
async def auth(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        raise error
    user = token['userinfo']
    if user:
        db_user = get_user_by_email(db=db, email=user['email'])
        if db_user:
            json_user = jsonable_encoder(db_user)
        else:
            user_schema = User()
            user_schema.email = user['email']
            user_schema.first_name = user['given_name']
            user_schema.last_name = user['family_name']
            user_schema.profile_picture_url = user['profile_picture']
            db_user = create_user(db=db, user=user_schema)
        request.session['user'] = json_user
    return RedirectResponse(url='/')


@router.get('/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/')
