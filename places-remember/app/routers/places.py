from typing import Annotated, Optional

from fastapi import Depends, APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from starlette import status

from ..schemas import Place as PlaceSchema
from ..dependencies import get_db, get_user
from ..crud.crud_places import create_place, get_place_by_id

templates = Jinja2Templates(directory="app/templates")

router = APIRouter(
    prefix='/place',
    tags=['place'],
    responses={404: {"description": "Not found"}}
)


@router.get("/get-place/{place_id}")
async def get_places(
    request: Request,
    place_id: int,
    db: Session = Depends(get_db),
    user: Optional[dict] = Depends(get_user)
):
    place = get_place_by_id(db=db, place_id=place_id)
    is_view = True
    return templates.TemplateResponse(
        "general/place.html",
        {"request": request, "user": user, "is_view": is_view, "place": place}
    )


@router.get("/add-place")
async def add_place_page(
    request: Request,
    user: Optional[dict] = Depends(get_user)
):
    return templates.TemplateResponse(
        "general/place.html",
        {"request": request, "user": user}
    )


@router.post("/add-place")
async def add_place(
    request: Request,
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    latitude: Annotated[float, Form()],
    longitude: Annotated[float, Form()],
    db: Session = Depends(get_db),
    user: Optional[dict] = Depends(get_user),
):
    place = PlaceSchema(
        title=title,
        description=description,
        latitude=latitude,
        longitude=longitude,
        author_id=user['id'],
    )
    db_post = create_place(
        place=place,
        db=db
    )
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
