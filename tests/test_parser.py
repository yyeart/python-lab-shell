import os
import pytest
from pyfakefs.fake_filesystem_unittest import Patcher
from pathlib import Path
from src import parser

@pytest.fixture
def create_ffs():
    patcher = Patcher()
    patcher.setUp()
    fs = patcher.fs
    fs.create_file('/root_file.txt', contents='123')
    fs.create_dir('/dir')
    fs.create_file('/dir/file.txt', contents='456')
    fs.create_dir('/dir/dir2')
    yield fs
    patcher.tearDown()

def test_parser_ls(create_ffs, capsys):
    cmd = 'ls /dir'
    parser.parse_command(cmd, logger=None)
    output = capsys.readouterr().out
    assert 'dir2' in output
    assert 'file.txt' in output

def test_parser_ls_nonexistent(create_ffs, capsys):
    cmd = 'ls /nonexistent'
    parser.parse_command(cmd, logger=None)
    output = capsys.readouterr().out
    assert 'ls: путь не найден' in output

def test_parser_cd(create_ffs):
    cmd = 'cd /dir'
    parser.parse_command(cmd, logger=None)
    assert Path(os.getcwd()).name == 'dir'

def test_parser_cd_too_many_args(create_ffs, capsys):
    cmd = 'cd /dir /dir2'
    parser.parse_command(cmd, logger=None)
    output = capsys.readouterr().out
    assert 'cd: слишком много аргументов' in output

def test_parser_cat(create_ffs, capsys):
    cmd = 'cat /dir/file.txt'
    parser.parse_command(cmd, logger=None)
    output = capsys.readouterr().out
    assert '456' in output

def test_parser_cat_no_args(create_ffs, capsys):
    parser.parse_command('cat', logger=None)
    output = capsys.readouterr().out
    assert 'cat: не указан(ы) аргумент(ы)' in output

def test_parser_cp_file(create_ffs, capsys):
    cmd = 'cp /dir/file.txt /dir/copy.txt'
    parser.parse_command(cmd, logger=None)
    assert os.path.exists('/dir/copy.txt')
    with open('/dir/copy.txt') as f:
        assert f.read() == '456'
    output = capsys.readouterr().out
    assert 'cp:' not in output

def test_parser_cp_dir_without_r_flag(create_ffs, capsys):
    cmd = 'cp /dir /copy'
    parser.parse_command(cmd, logger=None)
    output = capsys.readouterr().out
    assert '-r' in output

def test_parser_cp_dir(create_ffs):
    cmd = 'cp -r /dir /copy'
    parser.parse_command(cmd, logger=None)
    assert os.path.exists('copy/file.txt')
    with open('copy/file.txt') as f:
        assert f.read() == '456'

def test_parser_mv(create_ffs):
    cmd = 'mv /dir/file.txt /dir/new.txt'
    parser.parse_command(cmd, logger=None)
    assert not os.path.exists('/dir/file.txt')
    assert os.path.exists('/dir/new.txt')
    with open('/dir/new.txt') as f:
        assert f.read() == '456'

def test_parser_mv_nonexistent(create_ffs, capsys):
    cmd = 'mv /nonexistent.txt /new.txt'
    parser.parse_command(cmd, logger=None)
    output = capsys.readouterr().out
    assert 'не найден' in output

def test_parser_rm_file(create_ffs):
    cmd = 'rm /dir/file.txt'
    parser.parse_command(cmd, logger=None)
    assert not os.path.exists('/dir/file.txt')

def test_parser_rm_dir_without_r_flag(create_ffs, capsys):
    cmd = 'rm /dir'
    parser.parse_command(cmd, logger=None)
    output = capsys.readouterr().out
    assert '-r' in output

def test_parser_rm_dir_y(create_ffs, monkeypatch):
    cmd = 'rm -r /dir'

    monkeypatch.setattr('builtins.input', lambda y: 'y')

    parser.parse_command(cmd, logger=None)
    assert not Path('/dir').exists()

def test_parser_rm_dir_n(create_ffs, monkeypatch):
    cmd = 'rm -r /dir'

    monkeypatch.setattr('builtins.input', lambda n: 'n')

    parser.parse_command(cmd, logger=None)
    assert os.path.exists('/dir')

def test_parser_unknown_command(create_ffs, capsys):
    parser.parse_command('unknown', logger=None)
    output = capsys.readouterr().out
    assert 'Неизвестная команда: unknown' in output
