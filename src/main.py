import logging
import os
from src.config import LOGGING_CONFIG
from src.commands import ls, cd

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

def main() -> None:
    print('Для выхода используйте exit')

    while True:
        try:
            cmd = input(f'{os.getcwd()}> ').strip()
        except (EOFError, KeyboardInterrupt):
            print("\nВыход")
            break

        if not cmd:
            continue

        if cmd == 'exit':
            break

        split = cmd.split()
        command = split[0]
        args = split[1:]

        try:
            if command == 'ls':
                l_flag = '-l' in args
                path = next((a for a in args if a != '-l'), '.')
                ls.run_ls(path, l_flag)
            elif command == 'cd':
                if len(args) == 0:
                    path = None
                    extra_args = None
                else:
                    path = args[0]
                    extra_args = args[1:] if len(args) > 1 else None
                cd.run_cd(path, extra_args)
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
