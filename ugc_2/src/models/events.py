from datetime import datetime

from pydantic import BaseModel, Field


class UserEvent(BaseModel):
    user_id: str = Field(
        ..., description="ID пользователя, от которого получено событие"
    )
    movie_id: str | None = Field(..., description="ID фильма")
    

class Like(UserEvent):
    rating: int = Field(default=10)


class Bookmark(UserEvent):
    status: bool = Field(default=True)

