import logging
import zipfile
import tarfile
import os
from pathlib import Path

from src.errors import custom_error, perm_error, path_error

logger = logging.getLogger(__name__)

def validate_source(p: Path) -> bool:
    if not os.path.exists(p):
        path_error(p, 'zip')
        return False
    if not os.path.isdir(p):
        text = f'{p} - не каталог'
        custom_error(text)
        return False
    return True

def validate_zip(p: Path) -> bool:
    if not os.path.exists(p):
        path_error(p, 'unzip')
        return False
    if not zipfile.is_zipfile(p):
        text = f'unzip: {p} не является ZIP-архивом'
        custom_error(text)
        return False
    return True

def validate_tar(p: Path) -> bool:
    if not os.path.exists(p):
        path_error(p, 'untar')
        return False
    if not tarfile.is_tarfile(p):
        text = f'untar: {p} не является TAR-архивом'
        custom_error(text)
        return False
    return True

def run_zip(source: str, dest: str) -> None:
    s, d = Path(os.path.expanduser(source)), Path(os.path.expanduser(dest))
    try:
        if not validate_source(s):
            return
        with zipfile.ZipFile(d, 'w', zipfile.ZIP_DEFLATED) as zip:
            for dirpath, dirnames, filenames in os.walk(s):
                for filename in filenames:
                    file = Path(dirpath) / filename
                    arcname = file.relative_to(d.parent)
                    zip.write(file, arcname)
        logger.info(f'zip {os.path.abspath(s)} -> {os.path.abspath(d)}')

    except PermissionError as e:
        perm_error(e)

def run_unzip(path: str) -> None:
    p = Path(os.path.expanduser(path))
    try:
        if not validate_zip(p):
            return
        with zipfile.ZipFile(p, 'r') as zip:
            zip.extractall(os.getcwd())
        logger.info(f'unzip {os.path.abspath(p)} -> {os.getcwd()}')
    except PermissionError as e:
        perm_error(e)

def run_tar(source: str, dest: str) -> None:
    s, d = Path(os.path.expanduser(source)), Path(os.path.expanduser(dest))
    try:
        if not validate_source(s):
            return
        with tarfile.open(d, 'w:gz') as tar:
            tar.add(s, arcname=s.name)
        logger.info(f'tar {Path(os.path.abspath(s))} -> {Path(os.path.abspath(d))}')
    except PermissionError as e:
        perm_error(e)

def run_untar(path: str) -> None:
    p = Path(os.path.expanduser(path))
    try:
        if not validate_tar(p):
            return
        with tarfile.open(p, 'r:gz') as tar:
            tar.extractall(os.getcwd())
        logger.info(f'untar {os.path.abspath(p)} -> {os.getcwd()}')
    except PermissionError as e:
        perm_error(e)
