from fastapi import APIRouter, Depends, HTTPException
# from fastapi.openapi.utils import status_code_ranges
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from crud import users
from config.db_conf import get_db
from schemas.users import UserRequest

router = APIRouter(prefix="/api/user", tags= ["Users"])


@router.post("/register")
async def register(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    existing_user = await users.get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    user = await users.create_user(db, user_data)
    return {
        "code": 200,
        "message": "register success",
        "data":{
            "token": "wait",
            "user_info":{
                "id": user.id,
                "username": user.username,
                "bio": user.bio,
                "avatar": user.avatar,
            }
        }
    }
