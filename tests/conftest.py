import pytest
from pyfakefs.fake_filesystem import FakeFilesystem

@pytest.fixture
def fs(fs: FakeFilesystem) -> FakeFilesystem:
    return fs
