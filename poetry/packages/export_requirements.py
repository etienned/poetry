import io

from poetry.utils._compat import Path


def export_requirements(locker, path=None, dev=False, tag=False, egg=False):
    """Function to export a lock file to the requirements.txt format."""

    name = None
    if path is None:
        path = get_project_directory()
    else:
        path = Path(path)
        # Check if there's a file given in the path.
        if path.suffix:
            name = path.name
            path = path.parent

    if name is None:
        if dev:
            name = "requirements-dev.txt"
        else:
            name = "requirements.txt"

    installed_repo = locker.locked_repository(False)

    if dev:
        dev_installed_repo = locker.locked_repository(True)
        main_package_names = set(
            (package.name for package in installed_repo.packages)
        )
        packages = (
            package
            for package in dev_installed_repo.packages
            if package.name not in main_package_names
        )
    else:
        packages = installed_repo.packages

    output = []
    for package in packages:
        if package.source_type:
            egg_text = "#egg={}".format(package.name) if egg else ""
            name_version = "{}+{}@{}{}".format(
                package.source_type,
                package.source_url,
                package.version
                if (tag and package.version)
                else package.source_reference,
                egg_text,
            )
        else:
            name_version = "{}=={}".format(package.name, package.version)

        markers = str(package.marker.without_extras())
        if markers:
            markers = "; {}".format(markers)

        output.append("{}{}".format(name_version, markers))

    requirements = "\n".join(output)

    with io.open(path / name, "w", encoding="utf-8") as f:
        f.write(requirements)

    return path, name


def get_project_directory():
    cwd = Path.cwd()
    candidates = [cwd]
    candidates.extend(cwd.parents)

    for path in candidates:
        poetry_file = path / "pyproject.toml"

        if poetry_file.exists():
            return poetry_file.parent

    raise RuntimeError(
        "Poetry could not find a pyproject.toml file in {} or its parents".format(
            cwd
        )
    )
