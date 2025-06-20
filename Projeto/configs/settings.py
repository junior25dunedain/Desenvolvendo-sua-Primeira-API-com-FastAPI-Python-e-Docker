from pydantic_settings import BaseSetings
from pydantic import Field

class Settings(BaseSetings):
    DB_URL: str = Field(default='linkdobanco de dados')


settings = Settings()