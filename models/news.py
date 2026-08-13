from datetime import datetime
from typing import Optional
# from numba.core.types import Optional
from sqlalchemy import DateTime, Integer, String, Index, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        comment="create_time"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        comment="update_time"
    )




class Category(TimestampMixin, Base):
    __tablename__ = "news_category"
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="category_id"
    )
    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        comment="category_name"
    )
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False, comment="sort_order")

    def __repr__(self) -> str:
        return f"Category(id={self.id!r}, name={self.name!r}, sort_order={self.sort_order!r})"


class News(TimestampMixin, Base):
    __tablename__ = "news"

    # 创建索引： 提升查询速度
    __table_args__ = (
        Index("fk_news_category_idx", "category_id"),
        Index("idx_publish_time", "publish_time")
    )

    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="news_id")
    title: Mapped[str] = mapped_column(String(255), nullable= False, comment="news_title")
    description: Mapped[Optional[str]] = mapped_column(String(500), comment="news_description")
    content: Mapped[str] = mapped_column(String(5000), nullable=False, comment="news_content")
    image: Mapped[Optional[str]] = mapped_column(String(255), comment="news_home_image")
    author: Mapped[Optional[str]] = mapped_column(String(50), comment="news_author")
    category_id: Mapped[int] = mapped_column(Integer,ForeignKey("news_category.id"), nullable= False, comment="news_category_id")
    views: Mapped[int] = mapped_column(Integer, default= 0, nullable= False, comment="news_views")
    publish_time: Mapped[datetime] = mapped_column(DateTime, default= datetime.now, comment= "publish_time")

    def __repr__(self) -> str:
        return f"News(id={self.id!r}, title={self.title!r}, description={self.description!r}, content={self.content!r}, image={self.image!r}, author={self.author!r}, category_id={self.category_id!r}, views={self.views!r}, publish_time={self.publish_time!r})"
