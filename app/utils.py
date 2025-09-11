import bcrypt

bcrypt.__about__ = bcrypt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(pwd: str) -> str:
    return pwd_context.hash(pwd)


def verify(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
