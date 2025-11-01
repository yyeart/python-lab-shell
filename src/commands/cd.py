import logging
import os
from pathlib import Path
from src.config import LOGGING_CONFIG
from src.errors import path_error, perm_error

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

def run_cd(path: str | None = None) -> None:
    try:
        if not path:
            print(os.getcwd())
            return
        p = Path(path)
        expanded_path = os.path.expanduser(p)
        abs_path = os.path.abspath(expanded_path)
        os.chdir(abs_path)
        logger.info(f'cd {os.getcwd()}')
    except FileNotFoundError:
        path_error(p, 'cd')
    except NotADirectoryError:
        err = f'Ошибка: {p} - не каталог'
        print(err)
        logger.error(err)
    except PermissionError as e:
        perm_error(e)
