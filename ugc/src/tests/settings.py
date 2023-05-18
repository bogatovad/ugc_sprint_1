from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    clickhouse_table: str = Field('cinema_analytics.movie_views', env='CLICKHOUSE_TABLE')
    view_progress_url: str = Field('http://ugc_api:8000/api/v1/view_progress', env='VIEW_PROGRESS_URL')


test_settings = TestSettings()
