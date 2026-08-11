from datetime import datetime
from typing import Optional
# from numba.core.types import Optional
from sqlalchemy import Index, Integer, String, Enum, DateTime, ForeignKey
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
    password : Mapped[str] = mapped_column(String(255), comment= "密码（加密存储）")
    nickname : Mapped[Optional[str]] = mapped_column(String(50), comment= "昵称")
    avatar : Mapped[Optional[str]] = mapped_column(String(255), comment= "头像URL",
            default='https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg')
    gender: Mapped[Optional[str]] = mapped_column(Enum('male', 'female', 'unknown'), comment= "性别", default= "unknown")
    bio: Mapped[Optional[str]]= mapped_column(String(500), comment="个⼈简介", default='这个⼈很懒，什么都没留下')
    phone: Mapped[Optional[str]] = mapped_column(String(20), unique=True, comment="⼿机号")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), comment = "创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), onupdate=datetime.now(), comment = "更新时间")

    def __repr__(self):
        return f"User(id={self.id!r}, username={self.username!r}, nickname={self.nickname!r}, avatar={self.avatar!r}, gender={self.gender!r}, bio={self.bio!r}, phone={self.phone!r}, created_at={self.created_at!r}, updated_at={self.updated_at!r})"
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "nickname": self.nickname,
            "avatar": self.avatar,
            "gender": self.gender,
            "bio": self.bio,
            "phone": self.phone,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    class UserToken(Base):
        """
        ⽤户令牌表ORM模型
        """
        __tablename__ = 'user_token'
        # 创建索引
        __table_args__ = (
            Index('token_UNIQUE', 'token'),
            Index('fk_user_token_user_idx', 'user_id'),
        )
        id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement = True, comment = "令牌ID")
        user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), nullable = False, comment = "⽤户ID")
        token: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, comment="令牌值")
        expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False,
                                                     comment="过期时间")
        created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(), comment = "创建时间")

        def __repr__(self):
         return f"<UserToken(id={self.id}, user_id={self.user_id}, token='{self.token}')>"