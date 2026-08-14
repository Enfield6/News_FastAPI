from fastapi import APIRouter, Depends, HTTPException
# from fastapi.openapi.utils import status_code_ranges
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from crud import users
from config.db_conf import get_db
from schemas.users import UserRequest, UserAuthResponse, UserInfoResponse
from utils.response import success_response

router = APIRouter(prefix="/api/user", tags= ["Users"])


@router.post("/register")
async def register(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    existing_user = await users.get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户已存在")
    user = await users.create_user(db, user_data)
    token = await users.create_token(db, user.id)

    # return {
    #     "code": 200,
    #     "message": "register success",
    #     "data":{
    #         "token": token,
    #         "user_info":{
    #             "id": user.id,
    #             "username": user.username,
    #             "bio": user.bio,
    #             "avatar": user.avatar,
    #         }
    #     }
    # }
    response_data = UserAuthResponse(token= token, user_info=UserInfoResponse.model_validate(user))
    return success_response(message="注册成功", data= response_data)

