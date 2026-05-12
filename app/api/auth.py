from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.user import User

from app.schemas.auth import RegisterSchema
from app.schemas.auth import LoginSchema

from app.core.security import hash_password
from app.core.security import verify_password
from app.core.security import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/register")
def register(
    payload: RegisterSchema,
    db: Session = Depends(get_db)
):

    existing_user = (
        db.query(User)
        .filter(User.email == payload.email)
        .first()
    )

    if existing_user:
        return {
            "message": "User already exists"
        }

    user = User(
        username=payload.username,
        email=payload.email,
        password_hash=hash_password(payload.password)
    )

    db.add(user)

    db.commit()

    return {
        "message": "User created"
    }


@router.post("/login")
def login(
    payload: LoginSchema,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(User.email == payload.email)
        .first()
    )

    if not user:
        return {
            "message": "Invalid credentials"
        }

    if not verify_password(
        payload.password,
        user.password_hash
    ):
        return {
            "message": "Invalid credentials"
        }

    token = create_access_token(
        {"sub": user.email}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }