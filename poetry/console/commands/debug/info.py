import os
import sys

from ..command import Command


class DebugInfoCommand(Command):
    """
    Shows debug information.

    debug:info
    """

    def handle(self):
        poetry_python_version = ".".join(str(s) for s in sys.version_info[:3])

        self.output.title("Poetry")
        self.output.listing(
            [
                "<info>Version</info>: <comment>{}</>".format(self.poetry.VERSION),
                "<info>Python</info>:  <comment>{}</>".format(poetry_python_version),
            ]
        )

        self.call("env:info")
