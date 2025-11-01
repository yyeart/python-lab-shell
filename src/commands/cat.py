import logging
import os
from pathlib import Path
from src.config import LOGGING_CONFIG
from src.errors import path_error, perm_error, custom_error

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

def run_cat(path: str) -> None:
    p = Path(path)
    try:
        if not os.path.exists(p):
            path_error(p, 'cat')
            return
        if os.path.isdir(p):
            text = f'{p} - каталог'
            custom_error(text)
            return

        with open(p, 'r', encoding='utf-8') as f:
            content = f.read()
            print(content)
        logger.info(f'cat {os.path.abspath(p)}')

    except PermissionError as e:
        perm_error(e)

    except UnicodeDecodeError:
        text = f'Ошибка: невозможно прочитать файл: {p}'
        custom_error(text)
