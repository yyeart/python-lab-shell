from pyfakefs.fake_filesystem import FakeFilesystem # type: ignore

from src.commands import cat

def test_cat_for_nonexistent_path(fs: FakeFilesystem, capsys):
    path = 'nonexistent/file'
    cat.run_cat(path)
    output = capsys.readouterr().out
    assert 'путь не найден' in output.lower()

def test_cat_for_dir(fs: FakeFilesystem, capsys):
    fs.create_dir('data')
    cat.run_cat('data')
    output = capsys.readouterr().out
    assert 'каталог' in output.lower()

def test_cat(fs: FakeFilesystem, capsys):
    fs.create_dir('data')
    fs.create_file('data/text.txt', contents='content')
    cat.run_cat('data/text.txt')
    output = capsys.readouterr().out
    assert 'content' in output
