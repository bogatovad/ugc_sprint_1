from pydantic import BaseModel


class ViewProgress(BaseModel):
    user_id: str
    movie_id: str
    viewed_seconds: int

