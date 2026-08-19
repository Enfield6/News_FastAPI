import uuid
from datetime import timedelta, datetime

from fastapi import HTTPException
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.users import UserRequest, UserUpdateRequest
from utils import security
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


async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_username(db, username)
    if not user:
        return None
    if not security.verify_password(password, user.password):
        return None
    return user

async def get_user_by_token(db: AsyncSession, token: str):
    query = select(UserToken).where(UserToken.token == token)
    result = await db.execute(query)
    db_token = result.scalar_one_or_none()

    if not db_token or db_token.expires_at < datetime.now():
        return None

    query = select(User).where(User.id == db_token.user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def update_user(db: AsyncSession, username: str, user_data: UserUpdateRequest):

    query = update(User).where(User.username == username).values(** user_data.model_dump(
        exclude_unset= True,
        exclude_none= True
    ))
    result = await db.execute(query)
    await db.flush()

    if  result.rowcount == 0:
        raise HTTPException(status_code=404, detail= "用户不存在")

    updated_user = await get_user_by_username(db, username)
    return updated_user

async def chang_password(db: AsyncSession, user: User, old_password: str, new_password: str):
    if not security.verify_password(old_password, user.password):
        return False

    hashed_new_pwd = security.get_hash_password(new_password)
    user.password = hashed_new_pwd
    # 更新： 由SQLAlchemy真正接管这个User对象， 确保可以commit
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return True

