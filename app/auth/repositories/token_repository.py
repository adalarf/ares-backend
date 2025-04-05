from datetime import datetime
from sqlalchemy import select, and_, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.models.token import TokenModel
from app.auth.entities.user import Token


class TokenRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def create(self, user_id: int, access_token: str, refresh_token: str,
                    access_expires: datetime, refresh_expires: datetime) -> TokenModel:
        await self.deactivate_user_tokens(user_id)
        
        db_token = TokenModel(
            user_id=user_id,
            access_token=access_token,
            refresh_token=refresh_token,
            access_token_expires=access_expires,
            refresh_token_expires=refresh_expires
        )
        self.db.add(db_token)
        await self.db.commit()
        await self.db.refresh(db_token)
        return db_token


    async def get_by_access_token(self, access_token: str) -> TokenModel | None:
        query = select(TokenModel).where(
            and_(
                TokenModel.access_token == access_token,
                TokenModel.is_active == True,
                TokenModel.access_token_expires > datetime.utcnow()
            )
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()


    async def get_by_refresh_token(self, refresh_token: str) -> TokenModel | None:
        query = select(TokenModel).where(
            and_(
                TokenModel.refresh_token == refresh_token,
                TokenModel.is_active == True,
                TokenModel.refresh_token_expires > datetime.utcnow()
            )
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()


    async def deactivate_user_tokens(self, user_id: int) -> None:
        query = select(TokenModel).where(
            and_(
                TokenModel.user_id == user_id,
                TokenModel.is_active == True
            )
        )
        result = await self.db.execute(query)
        tokens = result.scalars().all()
        
        for token in tokens:
            token.is_active = False
        
        await self.db.commit()


    async def cleanup_expired_tokens(self) -> None:
        query = delete(TokenModel).where(
            and_(
                TokenModel.refresh_token_expires < datetime.utcnow(),
                TokenModel.is_active == True
            )
        )
        await self.db.execute(query)
        await self.db.commit() 