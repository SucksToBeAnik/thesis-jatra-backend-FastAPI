from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from typing import Annotated
from datetime import datetime, timezone, timedelta
from sqlmodel import Session, select
from models.users import User
from pydantic import BaseModel, model_validator, EmailStr
import jwt
from jwt import PyJWTError
from config.db import get_db_session
from config.settings import settings
from utils.helpers import verify_password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class LoginCredentials(BaseModel):
    email: EmailStr
    password: str

    @model_validator(mode="after")
    def validate_password(self):
        if len(self.password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return self


async def validate_login_credentials(
    login_credentials: LoginCredentials,
    token_expire_time: timedelta,
    db_session: Session = Depends(get_db_session),
):
    try:
        user = db_session.exec(
            select(User).where(User.email == login_credentials.email)
        ).first()
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid login credentials provided. User does not exist.",
            )

        if not verify_password(login_credentials.password, user.hashed_password):
            raise HTTPException(
                status_code=401, detail="Invalid password provided. Please try again."
            )

        token_expires_at = datetime.now(timezone.utc) + token_expire_time or timedelta(
            hours=24
        )

        data_to_encode = {"sub": user.email, "exp": token_expires_at}
        token = await generate_jwt_token(data_to_encode)
        return token
    except PyJWTError as e:
        raise HTTPException(status_code=500, detail=str(e))


secret_key = settings.secret_key


async def generate_jwt_token(data: dict):
    try:
        token = jwt.encode(data, key=secret_key, algorithm="HS256")
    except PyJWTError as e:
        raise HTTPException(status_code=500, detail=str(e))

    return token


async def get_authorized_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db_session: Session = Depends(get_db_session),
):
    try:

        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        exp = payload.get("exp")
        if exp is None:
            raise HTTPException(status_code=401, detail="Token expired")
        else:
            token_expires_at = datetime.fromtimestamp(exp, timezone.utc)
            if token_expires_at < datetime.now(timezone.utc):
                raise HTTPException(status_code=401, detail="Token expired")

        email = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=401, detail="Could not validate credentials"
            )

    except PyJWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    user = db_session.exec(select(User).where(User.email == email)).first()

    if user is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    return user
