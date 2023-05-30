from typing import Optional

from fastapi import Request, HTTPException

from .database import SessionLocal


# Database connection dependencie.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# User authorization dependencie.
async def get_user(request: Request) -> Optional[dict]:
    user = request.session.get('user')
    if user is not None:
        return user
    else:
        raise HTTPException(
            status_code=403,
            detail='Could not validate credentials.'
        )

    return None
