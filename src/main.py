import logging
import os
from src.config import LOGGING_CONFIG
from src.commands import ls, cd, cat, cp, mv, rm
from src.errors import too_many_args_error, no_args_error, not_enough_args_error

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


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

        try:
            if command == 'ls':
                l_flag = '-l' in args
                path = next((a for a in args if a != '-l'), '.')
                ls.run_ls(path, l_flag)
            elif command == 'cd':
                if len(args) > 1:
                    too_many_args_error('cd')
                elif len(args) == 0:
                    cd.run_cd()
                else:
                    path = args[0]
                    cd.run_cd(path)
            elif command == 'cat':
                if len(args) > 1:
                    too_many_args_error('cat')
                elif len(args) == 0:
                    no_args_error('cat')
                else:
                    path = args[0]
                    cat.run_cat(path)
            elif command == 'cp':
                if len(args) == 0:
                    no_args_error('cp')
                elif len(args) == 1:
                    not_enough_args_error('cp')
                elif len(args) > 3:
                    too_many_args_error('cp')
                elif len(args) == 2 and '-r' in args:
                    not_enough_args_error('cp -r')
                else:
                    if args[0] == '-r':
                        source = args[1]
                        dest = args[2]
                        r_flag = True
                    else:
                        source = args[0]
                        dest = args[1]
                        r_flag = False
                    cp.run_cp(source, dest, r_flag)
            elif command == 'mv':
                if len(args) > 2:
                    too_many_args_error('mv')
                elif len(args) == 1:
                    not_enough_args_error('mv')
                elif len(args) == 0:
                    no_args_error('mv')
                else:
                    source = args[0]
                    dest = args[1]
                    mv.run_mv(source, dest)
            elif command == 'rm':
                if len(args) > 2:
                    too_many_args_error('rm')
                elif len(args) == 0:
                    no_args_error('rm')
                elif len(args) == 1 and '-r' in args:
                    not_enough_args_error('rm -r')
                else:
                    if args[0] == '-r':
                        path = args[1]
                        r_flag = True
                    else:
                        path = args[0]
                        r_flag = False
                    rm.run_rm(path, r_flag)
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
