import logging
import os
from src.config import LOGGING_CONFIG
from src.errors import args_error, path_error, perm_error

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

def run_cat(path: str | None = None, extra_args: list[str] | None = None) -> None:
    try:
        if extra_args and len(extra_args) > 0:
            args_error()
            return
        if not path:
            err = 'Ошибка: файл не указан'
            print(err)
            logger.error(err)
            return
        if not os.path.exists(path):
            path_error(path)
            return
        if os.path.isdir(path):
            err = f'{path}: каталог'
            print(err)
            logger.error(err)
            return

        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            print(content)
        logger.info(f'cat {os.path.abspath(path)}')

    except PermissionError as e:
        perm_error(e)

    except UnicodeDecodeError:
        err = f'Ошибка: невозможно прочитать файл: {path}'
        print(err)
        logger.error(err)
