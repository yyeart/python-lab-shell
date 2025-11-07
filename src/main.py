import logging
from os import getcwd
from src.config import LOGGING_CONFIG
from src.parser import parse_command
from src.setup_logger import logger

logging.config.dictConfig(LOGGING_CONFIG)

def main() -> None:
    print('Для выхода используйте exit')

    while True:
        try:
            cmd = input(f'{getcwd()}> ').strip()
        except KeyboardInterrupt:
            print("\nВыход")
            break

        if not cmd:
            continue

        if cmd == 'exit':
            print('Выход')
            break

        try:
            parse_command(cmd, logger)
        except Exception as e:
            err = f'Ошибка выполнения команды "{cmd}": {e}'
            print(err)
            logger.exception(err)



if __name__ == '__main__':
    main()
