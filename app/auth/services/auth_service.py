from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from auth.repositories.user_repository import UserRepository
from auth.repositories.token_repository import TokenRepository
from auth.entities.user import User, UserCreate, UserLogin, Token, TokenData
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, user_repository: UserRepository, token_repository: TokenRepository):
        self.user_repository = user_repository
        self.token_repository = token_repository


    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)


    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)


    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt


    def create_refresh_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt


    async def authenticate_user(self, user_login: UserLogin) -> Optional[User]:
        user = await self.user_repository.get_by_email(user_login.email)
        if not user:
            return None
        if not self.verify_password(user_login.password, user.hashed_password):
            return None
        return user


    async def register_user(self, user_create: UserCreate) -> User:
        user = await self.user_repository.get_by_email(user_create.email)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        hashed_password = self.get_password_hash(user_create.password)
        return await self.user_repository.create(user_create, hashed_password)


    async def create_tokens(self, user: User) -> Token:
        access_expires = datetime.utcnow() + timedelta(minutes=30)
        refresh_expires = datetime.utcnow() + timedelta(days=7)

        access_token = self.create_access_token(
            data={"sub": user.email, "exp": access_expires}
        )
        refresh_token = self.create_refresh_token(
            data={"sub": user.email, "exp": refresh_expires}
        )

        await self.token_repository.create(
            user_id=user.id,
            access_token=access_token,
            refresh_token=refresh_token,
            access_expires=access_expires,
            refresh_expires=refresh_expires
        )

        return Token(
            access_token=access_token,
            refresh_token=refresh_token
        )


    async def verify_token(self, token: str) -> User:
        db_token = await self.token_repository.get_by_access_token(token)
        if not db_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )
        
        user = await self.user_repository.get_by_id(db_token.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        return user


    async def refresh_tokens(self, refresh_token: str) -> Token:
        db_token = await self.token_repository.get_by_refresh_token(refresh_token)
        if not db_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired refresh token"
            )

        user = await self.user_repository.get_by_id(db_token.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )

        return await self.create_tokens(user)
