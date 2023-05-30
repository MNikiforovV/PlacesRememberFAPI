from fastapi import Depends, APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from ..crud.crud_places import get_places_by_user
from ..dependencies import get_db

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


# Method renders main page. If user exists gets it's places data and
# sends it to template
@router.get("/", response_class=HTMLResponse)
async def root(request: Request, db: Session = Depends(get_db)):
    user = request.session.get('user')
    places = []
    if user:
        places = get_places_by_user(db=db, user_id=user['id'])
    response = templates.TemplateResponse(
            "general/index.html",
            {"request": request, "user": user, "places": places}
        )
    return response
