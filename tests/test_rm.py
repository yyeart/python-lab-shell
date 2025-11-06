import os

from pyfakefs.fake_filesystem import FakeFilesystem # type: ignore

from src.commands import rm

def test_rm_nonexistent_file(fs: FakeFilesystem, capsys):
    fs.create_dir('data')
    rm.run_rm('data/nonexistent.txt')
    output = capsys.readouterr().out
    assert 'не найден' in output

def test_rm_file(fs: FakeFilesystem, capsys):
    fs.create_dir('data')
    fs.create_file('data/file.txt', contents='123')
    rm.run_rm('data/file.txt')
    assert not os.path.exists('data/file.txt')
    output = capsys.readouterr().out
    assert 'rm:' not in output

def test_rm_file_with_r_flag(fs: FakeFilesystem, capsys):
    fs.create_file('file.txt', contents='123')
    rm.run_rm('file.txt', r_flag=True)
    output = capsys.readouterr().out
    assert 'не применим' in output
    assert os.path.exists('file.txt')

def test_rm_dir_without_r_flag(fs: FakeFilesystem, capsys):
    fs.create_dir('data')
    rm.run_rm('data')
    output = capsys.readouterr().out
    assert 'пропущен' in output
    assert os.path.exists('data')

def test_rm_dir_y(fs: FakeFilesystem, monkeypatch):
    fs.create_dir('data')
    monkeypatch.setattr('builtins.input', lambda y: 'y')
    rm.run_rm('data', r_flag=True)
    assert not os.path.exists('data')

def test_rm_dir_n(fs: FakeFilesystem, monkeypatch):
    fs.create_dir('data')
    monkeypatch.setattr('builtins.input', lambda n: 'n')
    rm.run_rm('data', r_flag=True)
    assert os.path.exists('data')


def test_rm_current_dir(fs: FakeFilesystem, capsys):
    fs.create_dir('/data')
    os.chdir('/data')
    rm.run_rm('/data', r_flag=True)
    output = capsys.readouterr().out
    assert 'нельзя удалить' in output
    assert os.path.exists('/data')

def test_rm_root_parent_dir(fs: FakeFilesystem, capsys):
    fs.create_dir('/root')
    rm.run_rm('/', r_flag=True)
    output = capsys.readouterr().out
    assert 'запрещено' in output
