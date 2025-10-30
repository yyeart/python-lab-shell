import logging
from src.config import LOGGING_CONFIG
from pathlib import Path

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

def not_found_error(path: str | Path | None, command: str):
    err = f'{command}: файл не найден - {path}'
    print(err)
    logger.error(err)

def path_error(path: str | Path | None, command: str) -> None:
    err = f'{command}: путь не найден - {path}'
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

def too_many_args_error(command: str) -> None:
    err = f'{command}: слишком много аргументов'
    print(err)
    logger.error(err)

def no_args_error(command: str) -> None:
    err = f'{command}: не указан аргумент'
    print(err)
    logger.error(err)
