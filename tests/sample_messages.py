# coding:utf-8

from pydantic import BaseModel
from qtmvvmtoolkit.commands import RelayCommand
from qtmvvmtoolkit.converters import IValueConverter
from qtmvvmtoolkit.inputs import (
    ObservableCollection,
    ObservableProperty,
)
from qtmvvmtoolkit.messenger import Message, Messenger
from qtmvvmtoolkit.objects import QtBindableObject
from qtpy.QtGui import *
from qtpy.QtWidgets import *


class User(BaseModel):
    name: str
    email: str

    @property
    def infos(self):
        return f"{self.name}->({self.email})"


class UserSelectedMessage(Message[User]): ...


class UserViewModel:
    def __init__(self):
        super().__init__()
        self.selected_user = ObservableProperty[User](User(name="", email=""))
        return None

    def command_display_user(self) -> None:
        return None


class UserToStrConverter(IValueConverter[User, str]):
    def convert(self, value: User) -> str:
        return value.infos


class HomeViewModel:
    def __init__(self):
        super().__init__()
        self.numbers = ObservableCollection[int](list(range(10)))
        self.state = ObservableProperty[bool](False)

        self.user_infos = ObservableCollection[User](
            [
                User(name="madara uchiwa", email="madara@uchiwa.de"),
                User(name="itachi uchiwa", email="itachi@uchiwa.ak"),
            ]
        )
        self.user = ObservableProperty[User](User(name="", email=""))

        Messenger.default().register(UserSelectedMessage, lambda v: print(v))
        ...

    def send_user_info(self) -> None:
        print("[x]:send user info")
        Messenger.default().send(UserSelectedMessage(self.user.get()))
        return None


class HomePage(QWidget, QtBindableObject):
    def __init__(self, vm: HomeViewModel) -> None:
        super().__init__()
        self.vm = vm

        self.initialize_component()
        self.initialize_binding()

        for number in self.vm.numbers:
            print(number)
        ...

    def initialize_component(self):
        lay = QHBoxLayout()
        lay.addStretch()

        layout = QVBoxLayout(self)
        layout.addLayout(lay)

        self.cboxNames = QComboBox(self)

        self.btn_send = QPushButton("Send User Infos")

        layout.addSpacing(10)

        layout.addWidget(self.btn_send)
        layout.addWidget(QLabel("<h2>Users</h2>"))
        layout.addWidget(self.cboxNames)
        layout.addStretch()

        return None

    def initialize_binding(self) -> None:
        self.binding_command(self.btn_send, RelayCommand(self.display_information))

        self.binding_selection(
            self.cboxNames,
            self.vm.user_infos,
            default_select=True,
            converter=UserToStrConverter(),
            observable_value=self.vm.user,
        )
        return None

    def display_information(self):
        self.vm.send_user_info()
        return None


class PageUser(QWidget, QtBindableObject):
    def __init__(self, vm: UserViewModel) -> None:
        super().__init__(None)
        self.vm = vm

        Messenger.default().register(UserSelectedMessage, self._update_user)

        layout = QVBoxLayout(self)

        self.btn_update = QPushButton("Update")
        self.label_userinfo = QLabel("--")

        layout.addWidget(self.btn_update)
        layout.addWidget(self.label_userinfo)

        self.initialize_bindings()
        ...

    def _update_user(self, user: User) -> None:
        self.vm.selected_user.set(user)
        return None

    def initialize_bindings(self) -> None:
        self.binding_label(self.label_userinfo, self.vm.selected_user)
        return None


if __name__ == "__main__":
    import sys

    from qdarktheme import load_palette, load_stylesheet

    app = QApplication([])
    app.setStyleSheet(load_stylesheet("auto"))
    app.setPalette(load_palette("auto"))

    page = QTabWidget()
    page.addTab(HomePage(HomeViewModel()), "Home")
    page.addTab(PageUser(UserViewModel()), "User")
    page.show()
    sys.exit(app.exec())
