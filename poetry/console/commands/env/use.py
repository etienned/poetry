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
            manager.deactivate(poetry.file.parent, self.output)

            return

        env = manager.activate(self.argument("python"), poetry.file.parent, self.output)

        self.line("Using virtualenv: <comment>{}</>".format(env.path))
