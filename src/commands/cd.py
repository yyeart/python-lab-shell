import logging
import os
from src.config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

def run_cd(path: str | None = None, extra_args: list[str] | None = None) -> None:
    try:
        if extra_args and len(extra_args) > 0:
            err = 'Ошибка: слишком много аргументов'
            print(err)
            logger.error(err)
            return
        if not path:
            print(os.getcwd())
            return
        expanded_path = os.path.expanduser(path)
        abs_path = os.path.abspath(expanded_path)
        os.chdir(abs_path)
        logger.info(f'cd {os.getcwd()}')
    except FileNotFoundError:
        err = f'Ошибка: такого пути нет - {path}'
        print(err)
        logger.error(err)
    except NotADirectoryError:
        err = f'Ошибка: {path} - не каталог'
        print(err)
        logger.error(err)
    except PermissionError:
        err = f'Ошибка: отказано в доступе - {path}'
        print(err)
        logger.error(err)
