import logging
import os
import shutil
from src.config import LOGGING_CONFIG
from src.errors import no_args_error, not_found_error, perm_error

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

def run_cp(source: str | None = None, dest: str | None = None, r_flag: bool = False) -> None:
    try:
        if not source or not dest:
            no_args_error('cp')
            return
        if not os.path.exists(source):
            not_found_error(source, 'cp')
            return

        if os.path.isdir(source):
            if not r_flag:
                err = f'cp: пропущен флаг -r для копирования каталога "{source}"'
                print(err)
                logger.error(err)
                return
            try:
                shutil.copytree(source, dest, dirs_exist_ok=True)
                logger.info(f'cp -r {os.path.abspath(source)} {os.path.abspath(dest)}')
            except PermissionError as e:
                perm_error(e)
            except Exception as e:
                err = f'cp: ошибка при копировании каталога - {e}'
                print(err)
                logger.error(err)
            return

        try:
            shutil.copy2(source, dest)
            logger.info(f'cp {os.path.abspath(source)} {os.path.abspath(dest)}')
        except PermissionError as e:
            perm_error(e)
        except IsADirectoryError:
            err = f'cp: {dest} - каталог'
            print(err)
            logger.error(err)
        except Exception as e:
            err = f'cp: ошибка при копировании файла - {e}'
            print(err)
            logger.error(err)

    except Exception as e:
        err = f'cp: неожижанная ошибка - {e}'
        print(err)
        logger.error(err)
