from datetime import datetime
from typing import Optional
# from numba.core.types import Optional
from sqlalchemy import DateTime, Integer, String, Index, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from .news import Base

class User(Base):
    """
    用户信息表ORM模型
    """
    __tablename__ = "user"
    __table_args__ = (
        Index("username_UNIQUE", "username"),
        Index("phone_UNIQUE", "phone")

    )

    id : Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment= "用户ID")
    username : Mapped[str] = mapped_column(String(20), comment= "用户名")
    password : Mapped[str] = mapped_column(String(255), comment= "密码")
    phone : Mapped[str] = mapped_column(String(11), comment= "手机号")
    email : Mapped[Optional[str]] = mapped_column(String(255), comment= "邮箱")
    create_time : Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment= "创建时间")
