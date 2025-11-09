import logging
import os
import re
from pathlib import Path
from src.errors import custom_error, perm_error, path_error

logger = logging.getLogger(__name__)

def grep_file(path: Path, pattern: str, flags: int) -> None:
    """
    Выполняет поиск строк в одном файле, соответствующих заданному шаблону.

    :param path: Путь к файлу или каталогу
    :type path: Path
    :param pattern: Регулярное выражение для поиска
    :type pattern: str
    :param flags: Флаги для ф-ции re.search
    :type flags: int
    """
    try:
        with open(path, 'r') as f:
            for line_number, line in enumerate(f, start=1):
                if re.search(pattern, line, flags):
                    print(f'{path}:{line_number}:{line.strip()}')
    except PermissionError as e:
        perm_error(e)

def run_grep(pattern: str, path: str, r_flag: bool = False, i_flag: bool = False) -> None:
    """
    Реализует команду 'grep' для поиска строк, соответствующих шаблону в файлах или каталогах.

    :param pattern: Регулярное выражение для поиска
    :type pattern: str
    :param path: Путь к файлу или каталогу
    :type path: str
    :param r_flag: Флаг для рекурсивного поиска
    :type r_flag: bool
    :param i_flag: Флаг для поиска без учета регистра
    :type i_flag: bool
    """
    p = Path(os.path.expanduser(path))
    if not os.path.exists(p):
        path_error(p, 'grep')

    flags = re.IGNORECASE if i_flag else 0
    try:
        if p.is_file():
            grep_file(p, pattern, flags)
        elif p.is_dir():
            if r_flag:
                for dirpath, dirnames, filenames in os.walk(p):
                    for filename in filenames:
                        grep_file(Path(dirpath) / filename, pattern, flags)
            else:
                for f in p.iterdir():
                    file_path = p / f
                    if file_path.is_file():
                        grep_file(file_path, pattern, flags)
        else:
            text = f'grep: Неверный путь - {p}'
            custom_error(text)
        logger.info(f'grep {"-r " if r_flag else ""}{"-i " if i_flag else ""}{pattern} {os.path.abspath(p)}')

    except PermissionError as e:
        perm_error(e)
