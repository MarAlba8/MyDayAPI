from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.config import settings
from database.database import get_db_session
from services.auth import JWTManager, UserManager
from schemas.auth import Token
from schemas.user import UserDBSchema


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_db_session),
):
    user_manager = UserManager(session=session)
    user = user_manager.authenticate_user(
        email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = UserDBSchema.model_validate(user)
    user_dict = user.model_dump(mode="json")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = JWTManager().create_access_token(
        data=user_dict, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
