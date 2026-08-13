import uuid
from datetime import timedelta, datetime

from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.users import UserRequest
from utils.security import get_hash_password
from models.news import Category, News
from models.users import User, UserToken


async def get_user_by_username(db: AsyncSession, username: str):
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, user_data: UserRequest):
    # 注册和 token 创建由请求级事务统一提交，避免只写入一半数据。
    hash_password = get_hash_password(user_data.password)
    user = User(username= user_data.username, password=hash_password)
    db.add(user)
    await db.flush()
    return user

async def create_token(db: AsyncSession, user_id: int):
    # 生成token + 增加过期时间 -> 查询数据库当前用户是否有token -> 有：更新；没有：添加
    token = str(uuid.uuid4())
    expires_at = datetime.now() + timedelta(days= 7)
    query = select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()

    if user_token:
        user_token.token = token
        user_token.expires_at = expires_at
    else:
        user_token = UserToken(user_id = user_id, token= token, expires_at= expires_at)
        db.add(user_token)
    await db.flush()

    return token
