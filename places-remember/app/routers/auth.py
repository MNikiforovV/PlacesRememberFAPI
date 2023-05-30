from fastapi import Depends, APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.encoders import jsonable_encoder

from starlette.config import Config
from starlette import status

from authlib.integrations.starlette_client import OAuth, OAuthError

from sqlalchemy.orm import Session

from ..settings import Settings
from ..crud.crud_user import get_user_by_email, create_user
from ..dependencies import get_db
from ..schemas import User

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


# Method sends request to google api,
# returns redirect to google login page
@router.get('/login')
async def login(request: Request):
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, str(redirect_uri))


# Method requests google access token and retrieves user information from it
# Then if user exists in database redirects to main page,
# if not creates new user in database with information from google token
@router.get('/auth')
async def auth(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        raise error
    user = token['userinfo']
    if user:
        db_user = get_user_by_email(db=db, email=user['email'])
        if not db_user:
            user_schema = User(
                email=user['email'],
                first_name=user['given_name'],
                last_name=user['family_name'],
                profile_picture_url=user['picture']
            )
            db_user = create_user(db=db, user=user_schema)
        json_user = jsonable_encoder(db_user)
        request.session['user'] = json_user
    return RedirectResponse(url='/')


# Method deletes user information from session, then redirects to main.
@router.get('/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/', status_code=status.HTTP_302_FOUND)
