import logging
import os
from shutil import rmtree
from pathlib import Path
from src.errors import custom_error, not_found_error, perm_error

logger = logging.getLogger(__name__)

def run_rm(path: str, r_flag: bool = False):
    """
    Удаляет файл или каталог\n
    Для удаления каталога необходим r_flag=True для рекурсивного удаления и подтверждение пользователя

    :param path: Путь
    :type path: str
    :param r_flag: Флаг для рекурсивного удаления
    :type r_flag: bool
    """
    p = Path(os.path.expanduser(path))
    abs_p = os.path.normpath(os.path.abspath(p))
    if not os.path.exists(p):
        not_found_error(p, 'rm')
        return
    cwd = os.path.abspath(os.getcwd())
    if abs_p in [os.path.abspath('/'), os.path.abspath('..')]:
        custom_error('rm: запрещено удалять корневой или родительский каталог')
        return

    if abs_p == cwd:
        custom_error('rm: нельзя удалить текущий каталог')
        return
    if p.is_file() and r_flag:
        text = 'rm: флаг -r не применим к файлу'
        custom_error(text)
        return
    if p.is_dir():
        if not r_flag:
            text = 'rm: пропущен флаг -r для удаления каталога'
            custom_error(text)
            return
        flag = True if input('rm: удалить каталог рекурсивно?(y/n) ').strip().lower() == 'y' else False
        if flag:
            try:
                rmtree(abs_p)
                logger.info(f'rm -r {os.path.abspath(p)}')
            except PermissionError as e:
                perm_error(e)
            except Exception as e:
                text = f'rm: ошибка при удалении каталога - {e}'
                custom_error(text)
            return
        else:
            return
    try:
        os.remove(p)
        logger.info(f'rm {os.path.abspath(p)}')
    except PermissionError as e:
        perm_error(e)
    except Exception as e:
        text = f'rm: ошибка при удалении файла - {e}'
        custom_error(text)
