import logging
import os
from pathlib import Path
from src.errors import path_error, perm_error

logger = logging.getLogger(__name__)

def empty_path(p: str | None) -> bool:
    if not p:
        print(os.getcwd())
        return True
    return False

def run_cd(path: str | None = None) -> None:
    try:
        if not empty_path(path):
            p = Path(path) # type: ignore[arg-type]
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
