from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.users import UserRequest
from utils.security import get_hash_password
from models.news import Category, News
from models.users import User


async def get_user_by_username(db: AsyncSession, username: str):
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, user_data: UserRequest):
    # 加密密码
    hash_password = get_hash_password(user_data.password)
    user = User(username= user_data.username, password=hash_password)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user