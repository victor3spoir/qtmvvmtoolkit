import sys
import typing

import context

context.__file__
from qtpy.QtWidgets import QMainWindow

from qtmvvmtoolkit.widgets.baseapp import BaseApp


class App(BaseApp):
    def __init__(self, appshell: typing.Type[QMainWindow]):
        super().__init__(sys.argv)
        self.appShell = appshell()
        self.appShell.show()
        return

    def launch(self):
        sys.exit(self.exec())
