from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    project_name: str = Field('ugc', env='PROJECT_NAME')
    host: str = Field("0.0.0.0", env="HOST")
    port: int = Field(8000, env="PORT")

settings = Settings()