import os
import importlib

from pyfakefs.fake_filesystem import FakeFilesystem

from src.commands import cp

def test_cp_for_nonexistent_file(fs: FakeFilesystem, capsys):
    source = "data/file1.txt"
    fs.create_dir("data")
    dest = "data/file2.txt"
    cp.run_cp(source, dest)
    output = capsys.readouterr().out
    assert "не найден" in output

def test_cp_file(fs: FakeFilesystem, capsys):
    fs.create_dir('data')
    fs.create_file('data/file1.txt', contents='123')
    importlib.reload(cp) #
    cp.run_cp('data/file1.txt', 'data/file2.txt')
    assert os.path.exists('data/file2.txt')
    with open('data/file2.txt') as f:
        assert f.read() == '123'
    output = capsys.readouterr().out
    assert 'cp:' not in output

def test_cp_dir_with_no_r_flag(fs: FakeFilesystem, capsys):
    fs.create_dir('data/folder')
    fs.create_file('data/folder/file.txt', contents='123')
    dest = 'data/dest'
    cp.run_cp('data/folder', dest, r_flag=False)
    output = capsys.readouterr().out
    assert 'пропущен' in output
    assert not os.path.exists(dest)

def test_cp_dir_with_r_flag(fs: FakeFilesystem):
    fs.create_dir('data/folder')
    fs.create_file('data/folder/file.txt', contents='123')
    dest = 'data/dest'
    cp.run_cp('data/folder', dest, r_flag=True)
    assert os.path.exists(dest)
    assert os.path.exists('data/dest/file.txt')
    with open('data/dest/file.txt') as f:
        assert f.read() == '123'

def test_cp_file_to_dir(fs: FakeFilesystem):
    fs.create_dir('data/dest')
    fs.create_file('data/file1.txt', contents='123')
    cp.run_cp('data/file1.txt', 'data/dest')
    dest_file = 'data/dest/file1.txt'
    assert os.path.exists(dest_file)
    with open(dest_file) as f:
        assert f.read() == '123'
