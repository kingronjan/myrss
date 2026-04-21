import logging
from os import PathLike
from pathlib import Path
from typing import Union

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.enums import DBType

BASE_DIR = Path(__file__).resolve().parent.parent.parent

AIO_DRIVERS = {
    DBType.SQLITE: 'aiosqlite',
}


class Settings(BaseSettings):
    DB_TYPE: DBType = DBType.SQLITE
    DB_PATH: PathLike = BASE_DIR / 'app.db'

    SQL_DEBUG: Union[bool, str] = False

    # log
    LOG_LEVEL: Union[int, str] = logging.INFO
    LOG_FORMAT: str = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'

    # mail
    MAIL_SENDER: str | None = None
    MAIL_PASSWORD: str | None = None
    MAIL_SMTP_SERVER: str | None = None
    MAIL_SMTP_PORT: int | None = None
    MAIL_RECEIVER: str | None = None

    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=BASE_DIR / '.env',
        env_file_encoding='utf-8',
        env_prefix='MYRSS_',
    )

    @property
    def db_url(self) -> str:
        driver = AIO_DRIVERS[self.DB_TYPE]
        return f'{self.db_type}+{driver}:///{self.DB_PATH}'

    @property
    def db_type(self):
        return self.DB_TYPE.value


settings = Settings()
