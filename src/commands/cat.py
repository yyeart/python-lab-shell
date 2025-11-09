import logging
import os
import sys
from pathlib import Path
from src.errors import path_error, perm_error, custom_error

logger = logging.getLogger(__name__)

def validate_path(p: Path) -> bool:
    """
    Проверяет, существует ли путь и не является ли он каталогом.

    :param p: Путь
    :type p: Path
    """
    if not os.path.exists(p):
        path_error(p, 'cat')
        return False
    if os.path.isdir(p):
        text = f'{p} - каталог'
        custom_error(text)
        return False
    return True

def run_cat(path: str) -> None:
    """
    Выводит содержимое файла\n
    Обрабатывает текстовые и бинарные файлы

    :param path: Путь
    :type path: str
    """
    p = Path(os.path.expanduser(path))
    try:
        if not validate_path(p):
            return
        bin_endings = ['bin', 'exe', 'dat', 'jpg', 'png', 'gif', 'zip']
        content: str | bytes = ''
        if p.suffix.lower()[1:] in bin_endings:
            with open(p, 'rb') as f:
                content = f.read()
            sys.stdout.buffer.write(content)
        else:
            with open(p, 'r', encoding='utf-8') as f:
                content = f.read()
                print(content)
        logger.info(f'cat {os.path.abspath(p)}')

    except PermissionError as e:
        perm_error(e)

    except UnicodeDecodeError:
        try:
            with open(p, 'rb') as f:
                content = f.read(64)
                print(content)
            logger.info(f'cat {os.path.abspath(p)}')
        except Exception as e:
            text = f'Ошибка: невозможно прочитать файл: {p} ({e})'
            custom_error(text)
