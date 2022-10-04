from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])


async def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
