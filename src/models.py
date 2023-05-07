from pydantic import BaseModel


class ViewHistory(BaseModel):
    user_id: str
    movie_id: str


class ViewProgress(BaseModel):
    user_id: str
    movie_id: str
    viewed_seconds: int

    @property
    def id(self):
        return f'{self.user_id}:{self.movie_id}'.encode()

