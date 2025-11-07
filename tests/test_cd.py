import os

from pyfakefs.fake_filesystem import FakeFilesystem

from src.commands import cd

def test_cd(fs: FakeFilesystem):
    fs.create_dir('data')
    os.chdir('/')
    cd.run_cd('data')
    assert os.getcwd().endswith('data')

def test_cd_for_nonexistent_dir(fs: FakeFilesystem, capsys):
    path = 'nonexistent/folder'
    cd.run_cd(path)
    output = capsys.readouterr().out
    assert 'путь не найден' in output.lower()

def test_cd_file(fs: FakeFilesystem, capsys):
    fs.create_dir('data')
    fs.create_file('data/test.txt')
    cd.run_cd('data/test.txt')
    output = capsys.readouterr().out
    assert 'не каталог' in output

def test_cd_no_arg(fs: FakeFilesystem, capsys):
    fs.create_dir('data')
    os.chdir('data')
    cd.run_cd()
    output = capsys.readouterr().out.strip()
    assert output.endswith('data')
