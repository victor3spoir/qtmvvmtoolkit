import context
from pages.homepage import PageHome
from pages.pageuser import PageUser

context.__file__

from PyQt6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from qtmvvmtoolkit.navigations import Navigator


class Routes:
    Home: str = "home"
    User: str = "user"


class AppShell(QMainWindow):
    def __init__(self):
        super().__init__()
        self.container = QWidget()
        self.outlet = QTabWidget(self)
        self.pageHome = PageHome()
        self.outlet.addTab(self.pageHome, "HomePage")
        self.pageUser = PageUser()
        self.outlet.addTab(self.pageUser, "UserPage")
        self.outlet.tabBar().hide()

        self.buttonHome = QPushButton("Home")
        self.buttonUser = QPushButton("User")

        Navigator.Current.add_outlet(self.outlet)
        Navigator.Current.add_route(Routes.Home, self.pageHome)
        Navigator.Current.add_route(Routes.User, self.pageUser)
        Navigator.Current.bind_navigation(self.buttonHome, Routes.Home)
        Navigator.Current.bind_navigation(self.buttonUser, Routes.User)

        navs = QHBoxLayout()
        navs.addWidget(self.buttonHome)
        navs.addWidget(self.buttonUser)
        navs.addStretch(10)
        layout = QVBoxLayout(self.container)

        self.setCentralWidget(self.container)
        layout.addLayout(navs)
        layout.addWidget(self.outlet)
