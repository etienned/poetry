from ..command import Command


class EnvUseCommand(Command):
    """
    Activate or create a new virtualenv for the current project.

    env:use
        {python : The python executable to use.}
    """

    def handle(self):
        from poetry.utils.env import EnvManager

        poetry = self.poetry
        manager = EnvManager(poetry.config)

        if self.argument("python") == "system":
            manager.deactivate(self.output, cwd=poetry.file.parent)

            return

        env = manager.activate(
            self.argument("python"), self.output, cwd=poetry.file.parent
        )

        self.line("Using virtualenv: <comment>{}</>".format(env.path))
