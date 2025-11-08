import os
import tarfile
import zipfile
from pyfakefs.fake_filesystem import FakeFilesystem

from src.commands.archive_commands import run_zip, run_unzip, run_tar, run_untar

def test_zip_unzip(fs: FakeFilesystem):
    fs.create_dir('/data/folder')
    fs.create_file('/data/folder/file.txt', contents='123')
    archive_path = '/data/archive.zip'
    run_zip('/data/folder', archive_path)
    assert os.path.exists(archive_path)
    assert zipfile.is_zipfile(archive_path)

    fs.create_dir('/data/unzip')
    os.chdir('/data/unzip')
    run_unzip(archive_path)
    assert os.path.exists('/data/unzip/folder/file.txt')

def test_zip_path_error(capsys):
    run_zip('/fake', '/path')
    output = capsys.readouterr().out
    assert 'путь не найден' in output

def test_zip_validation_error(fs: FakeFilesystem, capsys):
    fs.create_dir('/data')
    fs.create_file('/data/file.txt')
    run_zip('/data/file.txt', 'archive.zip')
    output = capsys.readouterr().out
    assert 'не каталог' in output

def test_unzip_path_error(capsys):
    run_unzip('/fake')
    output = capsys.readouterr().out
    assert 'путь не найден' in output

def test_unzip_validation_error(fs: FakeFilesystem, capsys):
    fs.create_dir('/data/folder')
    os.chdir('/data')
    run_unzip('/data/folder')
    output = capsys.readouterr().out
    assert 'не является' in output

def test_tar_untar(fs: FakeFilesystem):
    fs.create_dir('/data/folder')
    fs.create_file('/data/folder/file.txt', contents='123')
    archive_path = '/data/archive.tar.gz'
    run_tar('/data/folder', archive_path)
    assert os.path.exists(archive_path)
    assert tarfile.is_tarfile(archive_path)

    fs.create_dir('/data/untar')
    os.chdir('/data/untar')
    run_untar(archive_path)
    assert os.path.exists('/data/untar/folder/file.txt')

def test_tar_path_error(capsys):
    run_tar('/fake', '/path')
    output = capsys.readouterr().out
    assert 'путь не найден' in output

def test_tar_validation_error(fs: FakeFilesystem, capsys):
    fs.create_dir('/data')
    fs.create_file('/data/file.txt')
    run_tar('/data/file.txt', 'archive.tar')
    output = capsys.readouterr().out
    assert 'не каталог' in output

def test_untar_path_error(capsys):
    run_untar('/fake')
    output = capsys.readouterr().out
    assert 'путь не найден' in output

def test_untar_validation_error(fs: FakeFilesystem, capsys):
    fs.create_dir('/data/folder')
    os.chdir('/data')
    run_untar('/data/folder')
    output = capsys.readouterr().out
    assert 'не является' in output
