import logging
import os
from pathlib import Path
from src.errors import path_error, perm_error

logger = logging.getLogger(__name__)

def empty_path(p: str | None) -> bool:
    """
    Обработка случая, когда путь не задан

    :param p: Путь
    :type p: str | None
    """
    if not p:
        print(os.getcwd())
        return True
    return False

def run_cd(path: str | None = None) -> None:
    """
    Меняет текущую директорию на path.\n
    Если path не указан, выводит текущую директорию.\n

    :param path: Путь
    :type path: str | None
    """
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
