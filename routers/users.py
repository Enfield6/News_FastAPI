from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from schemas.users import UserRequest

router = APIRouter(prefix="/api/user", tags= ["Users"])


@router.post("/register")
async def register(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    return {
        "code": 200,
        "message": "register success",
        "data":{
            "token": "wait",
            "user_info":{
                "id": 1,
                "username": user_data.username,
                "bio": "null",
                "avatar": "",
            }
        }
    }
