import logging
import os
from shutil import copy2, copytree
from pathlib import Path
from src.errors import not_found_error, perm_error, custom_error

logger = logging.getLogger(__name__)

def run_cp(source: str, dest: str, r_flag: bool = False) -> None:
    """
    Копирует файл или каталог source в dest.\n
    Для каталогов требуется r_flag=True для рекурсивного копирования.

    :param source: Путь к файлу/каталогу
    :type source: str
    :param dest: Путь к копии
    :type dest: str
    :param r_flag: Флаг для рекурсивного копирования
    :type r_flag: bool
    """
    s, d = Path(os.path.expanduser(source)), Path(os.path.expanduser(dest))

    if not os.path.exists(s):
        not_found_error(s, 'cp')
        return

    if os.path.isdir(s):
        if not r_flag:
            text = f'cp: пропущен флаг -r для копирования каталога "{s}"'
            custom_error(text)
            return
        try:
            copytree(s, d, dirs_exist_ok=True)
            logger.info(f'cp -r {os.path.abspath(s)} {os.path.abspath(d)}')
        except PermissionError as e:
            perm_error(e)
        return

    if d.is_dir():
        d = d / s.name

    try:
        copy2(s, d)
        logger.info(f'cp {os.path.abspath(s)} {os.path.abspath(d)}')
    except PermissionError as e:
        perm_error(e)
    except IsADirectoryError:
        text = f'cp: {d} - каталог'
        custom_error(text)
