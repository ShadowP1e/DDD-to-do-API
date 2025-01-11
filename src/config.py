import os
from dataclasses import dataclass
from functools import lru_cache


@dataclass(frozen=True)
class Config:
    APP_NAME: str = 'DDD-Practice'

    # Database
    DB_HOST: str = os.getenv('DB_HOST', 'localhost')
    DB_USER: str = os.getenv('DB_USER', 'postgres')
    DB_PORT: str = os.getenv('DB_PORT', '5432')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD', 'postgres')
    DB_NAME: str = os.getenv('DB_NAME', 'postgres')

    # Auth

    # dataclass -> dict
    def to_dict(self):
        _dict = self.__dict__.copy()
        return _dict


@lru_cache(1)
def get_config() -> Config:
    return Config()
