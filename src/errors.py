import logging
from src.config import LOGGING_CONFIG
from pathlib import Path

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

def path_error(path: str | Path | None) -> None:
    err = f'Ошибка: путь не найден - {path}'
    print(err)
    logger.error(err)

def perm_error(e: PermissionError) -> None:
    err = f'Недостаточно прав: {e}'
    print(err)
    logger.warning(err)

def os_error(e: OSError) -> None:
    err = f'Системная ошибка: {e}'
    print(err)
    logger.error(err)

def args_error() -> None:
    err = 'Ошибка: слишком много аргументов'
    print(err)
    logger.error(err)
