# 整合 根据 token查询用户，返回用户
from fastapi import Header
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException
from config.db_conf import get_db
from models.users import User
from crud import users
from starlette import status

async def get_current_user(authorization: str = Header(..., alias= "Authorization"), db: AsyncSession = Depends(get_db)):
    # pass
    token = authorization.replace("Bearer", "").strip()
    user = await users.get_user_by_token(db, token)
    if not user:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= "无效的令牌或者是过期的令牌")
    return user

