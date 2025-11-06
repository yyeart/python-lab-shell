from src import errors

def test_custom_error(capsys):
    text = 'error'
    errors.custom_error(text)
    output = capsys.readouterr().out
    assert text in output

def test_not_found_error(capsys):
    errors.not_found_error('folder/fake_file.txt', 'ls')
    output = capsys.readouterr().out
    assert 'файл не найден' in output

def test_path_error(capsys):
    errors.path_error('folder/fake_folder', 'cd')
    output = capsys.readouterr().out
    assert 'путь не найден' in output

def test_perm_error(capsys):
    errors.perm_error(PermissionError('no access'))
    output = capsys.readouterr().out
    assert 'Недостаточно прав' in output

def test_os_error(capsys):
    errors.os_error(OSError('system error'))
    output = capsys.readouterr().out
    assert 'Системная ошибка' in output

def test_too_many_args_error(capsys):
    errors.too_many_args_error('cd')
    output = capsys.readouterr().out
    assert 'слишком много' in output

def test_no_args_error(capsys):
    errors.no_args_error('cat')
    output = capsys.readouterr().out
    assert 'не указан' in output

def test_not_enough_args_error(capsys):
    errors.not_enough_args_error('cp')
    output = capsys.readouterr().out
    assert 'недостаточно' in output
