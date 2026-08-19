from pydantic import BaseModel, Field, ConfigDict


class FavoriteCheckResponse(BaseModel):
    is_favorite: bool = Field(..., alias= "isFavorite")


class FavoriteAddRequest(BaseModel):
    news_id: int = Field(..., alias= "newsId")

class FavoriteListResponse(BaseModel):
    list: list[]
    total: int
    has_more: bool = Field(alias= "hasMore")

    model_config = ConfigDict(
        populate_by_name= True,
        validate_assignment= True
    )