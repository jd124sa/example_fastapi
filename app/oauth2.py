from time import timezone
import jwt
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session
from . import schemas, database, models
from fastapi import Depends, status, HTTPException

from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from .config import settings

# SECRET_KEY
# ALGORITHM
# expiration time

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encode_jwt


def verify_acces_token(token: str, credentials_execption):
    token_data = ""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_execption
        token_data = schemas.TokenData(id=id)

    except InvalidTokenError as e:
        # print(e)
        raise credentials_execption
    # except AssertionError as e:
    #     print(e)

    return token_data


# def get_current_user(token: str = Depends(oauth2_scheme)):
#     credentials_execption = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#
#     return verify_acces_token(token, credentials_execption)


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)
):
    credentials_execption = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = verify_acces_token(token, credentials_execption)
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
