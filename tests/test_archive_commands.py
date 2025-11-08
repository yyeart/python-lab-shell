import os
from pyfakefs.fake_filesystem import FakeFilesystem

from src.commands import archive_commands

def test_zip_unzip(fs: FakeFilesystem):
    fs.create_dir('data/folder')
    fs.create_file('data/folder/file.txt', contents='123')
    archive_path = 'data/archive.zip'
    archive_commands.run_zip('data/folder', archive_path)
    assert os.path.exists(archive_path)

    fs.create_dir('data/unzip')
    os.chdir('data/unzip')
    archive_commands.run_unzip(archive_path)
    assert os.path.exists('data/unzip/folder/file.txt')
