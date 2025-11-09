import logging
import os
import shutil
from pathlib import Path
from src.errors import custom_error, perm_error

logger = logging.getLogger(__name__)

def run_mv(source: str, dest: str) -> None:
    """
    Перемещает файл или каталог source в dest.

    :param source: Путь к файлу/каталогу
    :type source: str
    :param dest: Новый путь
    :type dest: str
    """
    s, d = Path(os.path.expanduser(source)), Path(os.path.expanduser(dest))
    try:
        if not os.path.exists(s):
            text = f'mv: Источник не найден - {s}'
            custom_error(text)
            return
        if not os.access(s, os.R_OK):
            text = f'mv: Нет прав на чтение - {s}'
            custom_error(text)
            return
        if os.path.exists(d) and not os.access(d, os.W_OK):
            text = f'mv: Нет прав на запись - {d}'
            custom_error(text)
            return

        if os.path.isdir(d):
            dest_dir = os.path.join(d, os.path.basename(s))
        else:
            dest_dir = str(d)

        shutil.move(s, dest_dir)
        logger.info(f'mv: {s} {dest_dir}')

    except PermissionError as e:
        perm_error(e)
