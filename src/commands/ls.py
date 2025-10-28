import stat
import time
import logging
from pathlib import Path
from src.config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

def format_mode(mode: int) -> str:
    perms = []
    for user in ['USR', 'GRP', 'OTH']:
        for act in ['R', 'W', 'X']:
            perms.append(user.lower() if mode & getattr(stat, f'S_I{act}{user}') else "-")
    return ''.join(perms)

def run_ls(path: str = '.', l_flag: bool = False) -> None:
    p = Path(path).resolve()
    try:
        if not p.exists():
            err = f'Ошибка: путь не найдет - {p}'
            print(err)
            logger.error(err)
            return

        if p.is_file():
            print(p.name)
            logger.info(f'ls {p} (файл)')
            return

        for item in p.iterdir():
            if l_flag:
                st = item.stat()
                permissions = format_mode(st.st_mode)
                size = st.st_size
                mtime = time.strftime("%Y-%m-%d %H:%M", time.localtime(st.st_mtime))
                print(f'{permissions:>10}    {size:>8}    {mtime}    {item.name}')
            else:
                print(item.name)
        logger.info(f'ls {"-l " if l_flag else ""}{p}')
    except PermissionError as e:
        err = f'Недостаточно прав: {e}'
        print(err)
        logger.error(err)
    except OSError as e:
        err = f'Системная ошибка: {e}'
        print(err)
        logger.error(err)
