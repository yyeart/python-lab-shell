import pytest # type: ignore
from pyfakefs.fake_filesystem import FakeFilesystem # type: ignore

@pytest.fixture
def fs(fs: FakeFilesystem) -> FakeFilesystem:
    return fs
