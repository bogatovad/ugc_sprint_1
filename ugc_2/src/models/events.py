from datetime import datetime

from pydantic import BaseModel, Field


class Event(BaseModel):
    movie_id: str | None = Field(..., description="ID фильма")


class UserEvent(Event):
    user_id: str = Field(
        ..., description="ID пользователя, от которого получено событие"
    )


class Like(UserEvent):
    rating: int = Field(default=10)


class Bookmark(UserEvent):
    status: bool = Field(default=True)


class Review(Event):
    text: str


class ReviewPosted(Review):
    user_id: str
    likes: list | None = Field(default=[], description="Лайки к рецензии")
    dislikes: list | None = Field(default=[], description="Дизлайки к рецензии")
    created_at: datetime = Field(default=datetime.now())
