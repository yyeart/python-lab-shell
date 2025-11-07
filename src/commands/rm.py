import logging
import os
from shutil import rmtree
from pathlib import Path
from src.errors import custom_error, not_found_error, perm_error

logger = logging.getLogger(__name__)

def run_rm(path: str, r_flag: bool = False):
    p = Path(os.path.expanduser(path))
    try:
        if not os.path.exists(p):
            not_found_error(p, 'rm')
            return
        if p.resolve() in [Path('/').resolve(), Path('..').resolve()]:
            text = 'rm: запрещено удалять корневой или родительский каталог'
            custom_error(text)
            return
        if p.resolve() == Path(os.getcwd()).resolve():
            text = 'rm: нельзя удалить текущий каталог'
            custom_error(text)
            return
        if p.is_file() and r_flag:
            text = 'rm: флаг -r не применим к файлу'
            custom_error(text)
            return
        if os.path.isdir(p):
            if not r_flag:
                text = 'rm: пропущен флаг -r для удаления каталога'
                custom_error(text)
                return
            flag = True if input('rm: удалить каталог рекурсивно?(y/n) ').lower() == 'y' else False
            if flag:
                try:
                    rmtree(p)
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

    except Exception as e:
        text = f'rm: неожиданная ошибка - {e}'
        custom_error(text)
