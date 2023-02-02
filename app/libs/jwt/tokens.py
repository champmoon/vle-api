from datetime import datetime, timedelta

from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTClaimsError, JWTError

from app.core.settings import settings


class JWTTokens:
    algorithm = settings.ALGORITHM

    access_token_lifetime = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    access_secret_key = settings.JWT_SECRET_KEY

    refresh_token_lifetime = settings.REFRESH_TOKEN_EXPIRE_MINUTES
    refresh_secret_key = settings.JWT_REFRESH_SECRET_KEY

    def __init__(self, data: dict) -> None:
        self.data = data

    def create_token(
        self,
        *,
        token_expire_minutes: float,
        secret_key: str,
        algorithm: str | None = None
    ) -> str:
        if algorithm is None:
            algorithm = self.algorithm

        to_encode = {
            "sub": self.data,
            "exp": datetime.utcnow() + timedelta(minutes=token_expire_minutes),
        }
        return jwt.encode(claims=to_encode, key=secret_key, algorithm=algorithm)

    def create_access_token(self) -> str:
        return self.create_token(
            token_expire_minutes=self.access_token_lifetime,
            secret_key=self.access_secret_key,
        )

    def create_refresh_token(self) -> str:
        return self.create_token(
            token_expire_minutes=self.refresh_token_lifetime,
            secret_key=self.refresh_secret_key,
        )

    def decode_token(
        self, *, token: str, secret_key: str, algorithm: str | None = None
    ) -> dict | None:
        if algorithm is None:
            algorithm = self.algorithm

        try:
            return jwt.decode(token=token, key=secret_key, algorithms=algorithm)
        except (JWTError, JWTClaimsError, ExpiredSignatureError):
            return None

    def decode_access_token(self, access_token: str) -> dict | None:
        return self.decode_token(token=access_token, secret_key=self.access_secret_key)

    def decode_refresh_token(self, refresh_token: str) -> dict | None:
        return self.decode_token(
            token=refresh_token, secret_key=self.refresh_secret_key
        )
