from .env_command import EnvCommand


class ExportCommand(EnvCommand):
    """
    Export locked packages to a requirements file at <path>

    export
        { path? : The path to create the requirements at. }
        { --D|dev : Export development packages. }
        { --T|tag : Use tag instead of commit hash for vcs packages. }
        { --E|egg : Add a egg name for vcs packages. }
    """

    help = """The export command export locked packages to a <comment>requirements.txt</> file.

If you do not specify a path, it will be saved along the pyproject.toml file.
"""

    def handle(self):
        from poetry.packages.export_requirements import export_requirements

        path = self.argument("path")
        dev = self.option("dev")
        tag = self.option("tag")
        egg = self.option("egg")

        path, name = export_requirements(
            self.poetry.locker, path, dev, tag, egg
        )

        self.line(
            "Created requirements <info>{}</> in <fg=blue>{}</>".format(
                name, path
            )
        )
