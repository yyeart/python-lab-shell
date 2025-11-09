import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def custom_error(text: str) -> None:
    """
    Выводит и логирует произвольную ошибку

    :param text: Текст для вывода
    :type text: str
    """
    err = f'{text}'
    print(err)
    logger.error(err)

def not_found_error(path: str | Path | None, command: str) -> None:
    text = f'{command}: файл не найден - {path}'
    custom_error(text)

def path_error(path: str | Path | None, command: str) -> None:
    text = f'{command}: путь не найден - {path}'
    custom_error(text)

def perm_error(e: PermissionError) -> None:
    text = f'Недостаточно прав: {e}'
    custom_error(text)

def os_error(e: OSError) -> None:
    text = f'Системная ошибка: {e}'
    custom_error(text)

def too_many_args_error(command: str) -> None:
    text = f'{command}: слишком много аргументов'
    custom_error(text)

def no_args_error(command: str) -> None:
    text = f'{command}: не указан(ы) аргумент(ы)'
    custom_error(text)

def not_enough_args_error(command: str) -> None:
    text = f'{command}: недостаточно аргументов'
    custom_error(text)
