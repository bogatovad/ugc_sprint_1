from pydantic import BaseSettings, Field


class TestSettings(BaseSettings):
    service_url: str = Field('http://tests_ugc_api:8000/api/v1/', env='UGC_HOST')
    clickhouse_table: str = Field('cinema_analytics.movie_views', env='CLICKHOUSE_TABLE')


test_settings = TestSettings()
