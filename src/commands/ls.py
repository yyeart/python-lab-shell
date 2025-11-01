import stat
import time
import logging
import os
from src.errors import path_error, perm_error, os_error
from pathlib import Path
from src.config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

def get_perms(mode: int) -> str:
    try:
        mode_str = stat.filemode(mode)
    except Exception:
        mode_str = oct(mode)
    return mode_str

def run_ls(path: str = '.', l_flag: bool = False) -> None:
    p = Path(os.path.expanduser(path))
    try:
        if not os.path.exists(p):
            path_error(p, 'ls')
            return

        if p.is_file():
            print(p.name)
            logger.info(f'ls {p} (файл)')
            return

        for item in p.iterdir():
            if l_flag:
                st = item.stat()
                permissions = get_perms(st.st_mode)
                size = st.st_size
                mtime = time.strftime("%Y-%m-%d %H:%M", time.localtime(st.st_mtime))
                print(f'{permissions:>10} {size:>8} {mtime} {item.name}')
            else:
                print(item.name)
        logger.info(f'ls {"-l " if l_flag else ""}{p}')
    except PermissionError as e:
        perm_error(e)
    except OSError as e:
        os_error(e)
