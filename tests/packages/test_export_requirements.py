import io

import pytest
import tempfile

from poetry.packages.export_requirements import export_requirements
from poetry.packages.locker import Locker
from poetry.packages.project_package import ProjectPackage

from ..helpers import get_package


@pytest.fixture
def locker():
    with tempfile.NamedTemporaryFile() as f:
        f.close()
        locker = Locker(f.name, {})

        return locker


@pytest.fixture
def root():
    return ProjectPackage("root", "1.2.3")


def test_requirements_file_is_written(locker, root):
    package_a = get_package("A", "1.0.0")
    package_a.add_dependency("B", "^1.0")
    package_a.hashes = ["456", "123"]
    packages = [package_a, get_package("B", "1.2")]

    locker.set_lock_data(root, packages)
    locker_path = locker.lock.path.parent
    export_requirements(locker, locker_path)
    path = locker_path / "requirements.txt"

    with io.open(path, encoding="utf-8") as f:
        content = f.read()

    expected = """a==1.0.0
b==1.2"""

    assert expected == content
