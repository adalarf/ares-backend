from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends  
from fastapi.security import OAuth2PasswordBearer
from app.auth.models.item import ItemModel
from app.auth.repositories.user_repository import UserRepository
from app.auth.repositories.token_repository import TokenRepository
from app.auth.repositories.item_repository import ItemRepository
from app.auth.entities.user import User, UserCreate, UserLogin, Token, UserUpdate, UserInfo
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.config import SECRET_KEY, ALGORITHM
from app.auth.models.user import UserModel
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import math



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class AuthService:
    def __init__(self, user_repository: UserRepository, token_repository: TokenRepository,
                 item_repository: ItemRepository):
        self.user_repository = user_repository
        self.token_repository = token_repository
        self.item_repository = item_repository


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


    async def update_user_stats(self, user_id: int, user_update: UserUpdate) -> User:
        updated_user = await self.user_repository.update_user(user_id, user_update)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return updated_user
    

    async def calculate_bmr(weight: float, height: float, age: int, gender: str):
        gender_coeff = 5 if gender == "male" else -161
        bmr = 10 * weight + 6.25 * height - 5 * age + gender_coeff
        return bmr
    

    async def calculate_tdee(bmr: float, activity_level: str):
        activity_coefficients = {
            "low": 1.2,
            "middle": 1.55,
            "high": 1.9
        }
        tdee = bmr * activity_coefficients.get(activity_level, 1.2)
        return tdee
    

    async def calculate_tef(tdee: float):
        tef = tdee / 0.9
        return tef
    

    async def get_user_info(self, user_id: int) -> UserInfo:
        user = await self.user_repository.get_user(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        level = math.floor((user.expirience / 50) ** 0.5) + 1
        experience_to_next_level = level ** 2 * 50
        user_info = UserInfo(
            id=user.id,
            gems=user.gems,
            level=level,
            experience_to_next_level=experience_to_next_level,
            experience_current=user.expirience
        )

        return user_info


    async def get_body_mass_index(self, weight: float, height: float) -> float:
        bmi = weight / ((height / 100) ** 2)
        return bmi
    

    async def get_user_avatar(self, user_id: int) -> str:
        user = await self.user_repository.get_user(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user.avatar
    
    
    async def buy_clothes(self, user_id: int, item_id: int) -> User:
        user = await self.user_repository.get_user(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        item = await self.item_repository.get_by_id(item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item not found"
            )
        
        if user.gems < int(item.price):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Not enough gems"
            )
        
        user.gems -= int(item.price)
        user.avatar = item.path
        await self.user_repository.update_user(user_id, user)
        return user
    

    async def set_user_avatar(self, user_data: User, path: str) -> User:
        user = await self.user_repository.get_user(user_data.id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        user_update = UserUpdate(avatar=path)
        updated_user = await self.user_repository.update_user(user.id, user_update)
        return updated_user
    

    async def get_items(self) -> list[ItemModel]:        
        items = await self.item_repository.get_all()
        return items
    

    async def get_user_items(self, user_id: int) -> list[ItemModel]:
        user = await self.user_repository.get_user(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        user_items = await self.item_repository.get_items_by_user_id(user_id)
        return user_items

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_async_session)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("sub")
        if user_email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    query = select(UserModel).options(selectinload(UserModel.restrictions)).where(UserModel.email == user_email)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return User.from_orm(user)
