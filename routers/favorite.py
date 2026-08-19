from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_conf import get_db
from models.users import User
from utils.auth import get_current_user
from utils.response import success_response

router = APIRouter(prefix="api/favorite", tags= ["favorite"])

@router.get("/check")
async def check_favorite(
        news_id: int = Query(..., alias= "newsId"),
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    return success_response(message= "检查收藏状态成功", data= {})
