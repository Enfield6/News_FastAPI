from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class UserRequest(BaseModel):
    username: str= Field(..., min_length=3, max_length=50)
    password: str= Field(..., min_length=3, max_length=50)



class UserInfoBase(BaseModel):
    """
    用户信息基础数据模型
    """
    nickname : Optional[str] = Field(None, max_length=50, description= "昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="头像URL")
    gender: Optional[str] = Field(None, max_length=10, description="性别")
    bio: Optional[str] = Field(None, max_length=500, description="个⼈简介")


class UserInfoResponse(UserInfoBase):
    """
    用户信息响应数据模型
    """
    id: int
    username: str
    model_config = ConfigDict(
        # populate_by_name = True,    # alias 字段名兼容
        from_attributes= True  # 允许从ORM对象中取值
    )



# data 数据类型
class UserAuthResponse(BaseModel):
    token: str
    user_info: UserInfoResponse = Field(..., alias= "userInfo")

    # 模型类配置
    model_config = ConfigDict(
        populate_by_name = True,    # alias 字段名兼容
        from_attributes= True  # 允许从ORM对象中取值
    )


class UserUpdateRequest(BaseModel):
    nickname: str = Field(default=None)
    avatar: str = Field(default=None)
    gender: str = Field(default= None)
    bio: str = Field(default= None)
    phone: str = Field(default= None)
