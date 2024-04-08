from datetime import datetime, timedelta, timezone
from src.app.config.config import JWT_SECRET_KEY, ALGORITHM
from jose import jwt


def encode_user(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key=JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_user(token: str):
    decoded_data = jwt.decode(token, key=JWT_SECRET_KEY, algorithms=ALGORITHM)
    return decoded_data
