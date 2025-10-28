import logging
from src.config import LOGGING_CONFIG
from src.commands import ls

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

def main() -> None:
    print('Для выхода используйте exit')

    while True:
        try:
            cmd = input("> ").strip()
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
