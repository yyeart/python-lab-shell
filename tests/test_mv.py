import os

from pyfakefs.fake_filesystem import FakeFilesystem

from src.commands import mv

def test_mv_nonexistent_file(fs: FakeFilesystem, capsys):
    fs.create_dir('data')
    mv.run_mv('data/nonexistent.txt', 'data/file.txt')
    output = capsys.readouterr().out
    assert 'не найден' in output
    assert not os.path.exists('data/file.txt')

def test_mv_file(fs: FakeFilesystem, capsys):
    fs.create_dir('data')
    fs.create_file('data/file1.txt', contents='123')
    mv.run_mv('data/file1.txt', 'data/file2.txt')
    assert not os.path.exists('data/file1.txt')
    assert os.path.exists('data/file2.txt')
    with open('data/file2.txt') as f:
        assert f.read() == '123'
    output = capsys.readouterr().out
    assert 'mv:' not in output

def test_mv_into_existing_folder(fs: FakeFilesystem):
    fs.create_dir('folder')
    fs.create_dir('folder2')
    fs.create_file('folder/file.txt', contents='123')
    mv.run_mv('folder/file.txt', 'folder2')
    assert not os.path.exists('folder/file.txt')
    assert os.path.exists('folder2/file.txt')
    with open('folder2/file.txt') as f:
        assert f.read() == '123'

def test_mv_folder(fs: FakeFilesystem, capsys):
    fs.create_dir('folder1')
    fs.create_dir('folder2')
    fs.create_file('folder1/file.txt', contents='123')
    mv.run_mv('folder1', 'folder2')
    assert not os.path.exists('folder1')
    assert os.path.exists('folder2/folder1/file.txt')
    with open('folder2/folder1/file.txt') as f:
        assert f.read() == '123'

def test_mv_no_read_perm(fs: FakeFilesystem, capsys):
    fs.create_dir('/data')
    fs.create_file('/data/file.txt', contents='123')
    fs.chmod('/data/file.txt', 0)
    mv.run_mv('/data/file.txt', '/data/new.txt')
    output = capsys.readouterr().out
    assert 'Недостаточно прав' in output or 'Нет прав на чтение' in output
    assert os.path.exists('/data/file.txt')

def test_mv_no_write_perm(fs: FakeFilesystem, capsys):
    fs.create_dir('/src')
    fs.create_dir('/dest')
    fs.create_file('/src/file.txt', contents='123')
    fs.create_file('/dest/file.txt', contents='456')
    fs.chmod('/dest/file.txt', 0)
    mv.run_mv('/src/file.txt', '/dest/file.txt')
    output = capsys.readouterr().out
    assert 'Нет прав на запись' in output
    assert os.path.exists('/src/file.txt')
