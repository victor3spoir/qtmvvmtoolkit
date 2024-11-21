# import qdarktheme

from app import App
from appshell import AppShell


class Program:
    def __init__(self):
        self.app = App(AppShell)
        self.app.configureApplication("testapp", "1.0.0", 500)
        self.app.centerWindow()
        # self.app.setStyleSheet(qdarktheme.load_stylesheet("auto"))
        # self.app.setPalette(qdarktheme.load_palette("auto"))
        self.app.launch()
        return
