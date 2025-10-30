import logging
import os
from src.config import LOGGING_CONFIG
from src.errors import path_error, too_many_args_error, perm_error

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

def run_cd(path: str | None = None, extra_args: list[str] | None = None) -> None:
    try:
        if extra_args and len(extra_args) > 0:
            too_many_args_error('cd')
            return
        if not path:
            print(os.getcwd())
            return
        expanded_path = os.path.expanduser(path)
        abs_path = os.path.abspath(expanded_path)
        os.chdir(abs_path)
        logger.info(f'cd {os.getcwd()}')
    except FileNotFoundError:
        path_error(path, 'cd')
    except NotADirectoryError:
        err = f'Ошибка: {path} - не каталог'
        print(err)
        logger.error(err)
    except PermissionError as e:
        perm_error(e)
