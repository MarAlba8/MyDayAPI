from datetime import datetime, timedelta, timezone
from typing import Annotated, Dict
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError

from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm.session import Session

from core.config import settings
from database.models.user import User
from schemas.auth import TokenData
from database.database import get_db_session
from schemas.user import UserDBSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserManager:
    def __init__(self, session: Session | None = None):
        self.session = session

    def hash_password(self, password: str):
        hashed_password = pwd_context.hash(secret=password)
        return hashed_password

    def get_user(self, email: str) -> User:
        query = select(User).filter(User.email == email)
        return self.session.execute(query).scalars().first()

    def verify_password(self, hashed_password: str, password: str):
        return pwd_context.verify(password, hashed_password)

    def authenticate_user(self, email: str, password: str):
        db_user = self.get_user(email)
        if not db_user:
            return False

        password_verified = self.verify_password(
            password=password, hashed_password=db_user.password
        )
        if not password_verified:
            return False
        return db_user


class JWTManager:
    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None) -> Dict:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)

        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Session = Depends(get_db_session),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email = payload.get("email")
        if not email:
            raise credentials_exception
        token_data = TokenData(email=email)
    except InvalidTokenError as e:
        credentials_exception.detail = e.args[0]
        raise credentials_exception

    user_manager = UserManager(session)
    user = user_manager.get_user(email=token_data.email)
    if not user:
        raise credentials_exception
    return UserDBSchema.model_validate(user)
