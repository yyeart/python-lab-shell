from src.commands import archive_commands, grep, rm, mv, ls, cp, cd, cat
from src.errors import too_many_args_error, no_args_error, not_enough_args_error

def parse_command(cmd: str, logger):
    """
    Разбивает строку cmd на команды и аргументы\n
    Вызывает соответствующие функции и обрабатывает ошибки

    :param cmd: Команда пользователя
    :type cmd: str
    :param logger: Журнал действий
    :type logger: Any
    """
    split = cmd.split()
    command = split[0]
    args = split[1:]

    if command == 'ls':
        l_flag = '-l' in args
        if l_flag and len(args) > 2:
            too_many_args_error(command)
        if not l_flag and len(args) > 1:
            too_many_args_error(command)
        path = next((a for a in args if a != '-l'), '.')
        ls.run_ls(path, l_flag)
    elif command == 'cd':
        if len(args) > 1:
            too_many_args_error(command)
        elif len(args) == 0:
            cd.run_cd()
        else:
            path = args[0]
            cd.run_cd(path)
    elif command == 'cat':
        if len(args) > 1:
            too_many_args_error(command)
        elif len(args) == 0:
            no_args_error(command)
        else:
            path = args[0]
            cat.run_cat(path)
    elif command == 'cp':
        if len(args) == 0:
            no_args_error(command)
        elif len(args) == 1:
            not_enough_args_error(command)
        elif len(args) > 3:
            too_many_args_error(command)
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
            too_many_args_error(command)
        elif len(args) == 1:
            not_enough_args_error(command)
        elif len(args) == 0:
            no_args_error(command)
        else:
            source = args[0]
            dest = args[1]
            mv.run_mv(source, dest)
    elif command == 'rm':
        if len(args) > 2:
            too_many_args_error(command)
        elif len(args) == 0:
            no_args_error(command)
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
    elif command == 'zip':
        if len(args) > 2:
            too_many_args_error(command)
        elif len(args) == 1:
            not_enough_args_error(command)
        elif len(args) == 0:
            no_args_error(command)
        else:
            source = args[0]
            dest = args[1]
            archive_commands.run_zip(source, dest)
    elif command == 'unzip':
        if len(args) > 1:
            too_many_args_error(command)
        elif len(args) == 0:
            no_args_error(command)
        else:
            path = args[0]
            archive_commands.run_unzip(path)
    elif command == 'tar':
        if len(args) > 2:
            too_many_args_error(command)
        elif len(args) == 1:
            not_enough_args_error(command)
        elif len(args) == 0:
            no_args_error(command)
        else:
            source = args[0]
            dest = args[1]
            archive_commands.run_tar(source, dest)
    elif command == 'untar':
        if len(args) > 1:
            too_many_args_error(command)
        elif len(args) == 0:
            no_args_error(command)
        else:
            path = args[0]
            archive_commands.run_untar(path)
    elif command == 'grep':
        if len(args) == 0:
            no_args_error(command)
        elif len(args) == 1:
            not_enough_args_error(command)
        elif len(args) > 4:
            too_many_args_error(command)
        else:
            r_flag = '-r' in args
            i_flag = '-i' in args
            flags = [a for a in args if a in ['-r', '-i']]
            args_no_flags = [a for a in args if a not in flags]
            if len(args_no_flags) < 2:
                not_enough_args_error(command)
            pattern, path = args_no_flags[0], args_no_flags[1]
            grep.run_grep(pattern, path, r_flag, i_flag)
    else:
        err = f'Неизвестная команда: {command}'
        print(err)
        try:
            logger.warning(err)
        except AttributeError:
            print('no logger found')
