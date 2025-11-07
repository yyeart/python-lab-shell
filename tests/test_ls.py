import os.path

from pyfakefs.fake_filesystem import FakeFilesystem

from src.commands import ls

def test_ls_for_nonexistent_path(fs: FakeFilesystem, capsys):
    path = 'nonexistent/folder'
    ls.run_ls(path)
    output = capsys.readouterr().out
    assert 'путь не найден' in output.lower()

def test_ls_for_file(fs: FakeFilesystem, capsys):
    fs.create_dir('data')
    fs.create_file(os.path.join('data', 'file.txt'), contents='test')
    ls.run_ls('data/file.txt')
    output = capsys.readouterr().out.strip()
    assert output == 'file.txt'

def test_ls_for_empty_dir(fs: FakeFilesystem, capsys):
    fs.create_dir('data')
    ls.run_ls('data')
    output = capsys.readouterr().out.strip()
    assert output == ''

def test_ls_for_dir(fs: FakeFilesystem, capsys):
    fs.create_dir('data')
    fs.create_file(os.path.join('data', 'a.txt'))
    fs.create_file(os.path.join('data', 'b.log'))
    fs.create_dir(os.path.join('data', 'subfolder'))
    ls.run_ls('data')
    output = capsys.readouterr().out.strip().split('\n')
    assert set(output) == {'a.txt', 'b.log', 'subfolder'}

def test_ls_l_flag(fs: FakeFilesystem, capsys):
    fs.create_dir('data')
    fs.create_file('data/a.txt', contents='test')
    ls.run_ls('data', l_flag=True)
    output = capsys.readouterr().out.strip()
    assert 'a.txt' in output
    assert len(output.split()) >= 4
