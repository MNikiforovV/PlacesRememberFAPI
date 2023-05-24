from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def root(request: Request):
    user = request.session.get('user')
    return templates.TemplateResponse(
        "general/index.html",
        {"request": request, "user": user}
    )


@router.get("/about")
async def about():
    return {"message": "This will be page with info about site"}
