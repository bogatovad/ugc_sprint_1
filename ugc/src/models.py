from datetime import datetime

from pydantic import BaseModel, Field


class Event(BaseModel):
    user_id: str = Field(..., description='ID пользователя, от которого получено событие')
    type: str = Field(..., description='Тип события', example='view_progress')
    movie_id: str | None = Field(..., description='ID фильма')
    movie_timestamp: int | None = Field(..., description='Отсмотренный фрейм')


class EventPosted(Event):
    created_at: str = Field(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))




