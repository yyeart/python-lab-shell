import os

from pyfakefs.fake_filesystem import FakeFilesystem # type: ignore

from src.commands import cp

def test_cp_for_nonexistent_file(fs: FakeFilesystem, capsys):
    source = "data/file1.txt"
    fs.create_dir("data")
    dest = "data/file2.txt"
    cp.run_cp(source, dest)
    output = capsys.readouterr().out
    assert "не найден" in output

def test_cp_file(fs: FakeFilesystem, capsys):
    fs.create_dir('/data')
    fs.create_file('/data/file1.txt', contents='123')
    cp.run_cp('/data/file1.txt', '/data/file2.txt')
    assert os.path.exists('/data/file2.txt')
    with open('/data/file2.txt') as f:
        assert f.read() == '123'
    output = capsys.readouterr().out
    assert 'cp:' not in output
