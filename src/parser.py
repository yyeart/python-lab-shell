from src.commands import archive_commands, rm, mv, ls, cp, cd, cat
from src.errors import too_many_args_error, no_args_error, not_enough_args_error

def parse_command(cmd: str, logger):
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
    else:
        err = f'Неизвестная команда: {command}'
        print(err)
        try:
            logger.warning(err)
        except AttributeError:
            print('no logger found')
