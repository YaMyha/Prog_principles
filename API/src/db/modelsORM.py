from datetime import datetime, timezone
from typing import Annotated, Optional, List

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import String, text, ForeignKey, MetaData, Integer, TIMESTAMP, Boolean
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship

str_256 = Annotated[str, 256]
intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"),
    onupdate=datetime.utcnow,
)]

metadata = MetaData()


class Base(DeclarativeBase):
    type_annotation_map = {
        str_256: String(256)
    }

    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"
    metadata = metadata

    id: Mapped[intpk]
    username: Mapped[str] = mapped_column(
        String, unique=True, index=True, nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    rating: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[created_at]
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    posts: Mapped[List["Post"]] = relationship(
        "Post",
        back_populates="author",
    )


class Post(Base):
    __tablename__ = "post"
    metadata = metadata

    id: Mapped[intpk]
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))
    title: Mapped[str_256]
    # TO DO: change type of description
    description: Mapped[str]
    tags: Mapped[Optional[str]]
    # comments: Mapped[list["CommentsORM"]] = relationship()
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    author: Mapped["User"] = relationship(
        "User",
        back_populates="posts",
    )

# class CommentsORM(Base):
#     __tablename__ = "comments"
#
#     id: Mapped[intpk]
#     author_id: Mapped[str]
#     text: Mapped[str]
#     created_at: Mapped[created_at]
#     updated_at: Mapped[updated_at]
#
#     author: Mapped["UsersORM"] = relationship()
