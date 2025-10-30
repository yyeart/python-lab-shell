import logging
import os
from src.config import LOGGING_CONFIG
from src.commands import ls, cd, cat

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

def check_args(args) -> tuple[str | None, list[str] | None]:
    if len(args) == 0:
        path = None
        extra_args = None
    else:
        path = args[0]
        extra_args = args[1:] if len(args) > 1 else None
    return path, extra_args

def main() -> None:
    print('Для выхода используйте exit')

    while True:
        try:
            cmd = input(f'{os.getcwd()}> ').strip()
        except KeyboardInterrupt:
            print("\nВыход")
            break

        if not cmd:
            continue

        if cmd == 'exit':
            print('Выход')
            break

        split = cmd.split()
        command = split[0]
        args = split[1:]
        path, extra_args = check_args(args)

        try:
            if command == 'ls':
                l_flag = '-l' in args
                path = next((a for a in args if a != '-l'), '.')
                ls.run_ls(path, l_flag)
            elif command == 'cd':
                cd.run_cd(path, extra_args)
            elif command == 'cat':
                cat.run_cat(path, extra_args)
            else:
                err = f'Неизвестная команда: {command}'
                print(err)
                logger.warning(err)
        except Exception as e:
            err = f'Ошибка выполнения команды "{cmd}": {e}'
            print(err)
            logger.exception(err)

if __name__ == '__main__':
    main()
