import context
from pages.homepage import HomePage

context.__file__

from qtpy.QtWidgets import QMainWindow


class AppShell(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setCentralWidget(HomePage())
        pass
