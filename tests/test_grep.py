from pyfakefs.fake_filesystem import FakeFilesystem
from src.commands import grep

def normalize_path(s: str) -> str:
    return s.replace('\\', '/')

def test_grep_file(fs: FakeFilesystem, capsys):
    fs.create_dir('/data')
    fs.create_file('/data/file.txt', contents='hello\nworld')
    grep.run_grep('hello', '/data/file.txt')
    output = normalize_path(capsys.readouterr().out)
    assert '/data/file.txt:1:hello' in output

def test_grep_i_flag(fs: FakeFilesystem, capsys):
    fs.create_dir('/data')
    fs.create_file('/data/file.txt', contents='hello\nworld\nHELLO\nworld')
    grep.run_grep('hello', '/data/file.txt', i_flag=True)
    output = normalize_path(capsys.readouterr().out)
    assert output.count('file.txt') == 2

def test_grep_r_flag(fs: FakeFilesystem, capsys):
    fs.create_dir('/data/folder')
    fs.create_file('/data/file1.txt', contents='hello world')
    fs.create_file('/data/folder/file2.txt', contents='hello casino')
    grep.run_grep('hello', '/data', r_flag=True)
    output = normalize_path(capsys.readouterr().out)
    assert 'file1.txt' in output and 'file2.txt' in output

def test_grep_no_matches(fs: FakeFilesystem, capsys):
    fs.create_dir('/data')
    fs.create_file('/data/file.txt', contents='world')
    grep.run_grep('hello', '/data/file.txt')
    output = capsys.readouterr().out
    assert output.strip() == ''

def test_grep_path_error(capsys):
    grep.run_grep('casino', "no/casino/:'(")
    output = capsys.readouterr().out
    assert 'путь не найден' in output
