# coding:utf-8
from pages.templates.PageUser_ui import Ui_PageUser
from qtmvvmtoolkit.objects import QtBindableObject
from qtpy.QtWidgets import QWidget
from viewmodels.uservm import UserViewModel


class PageUser(QWidget, Ui_PageUser, QtBindableObject):
    def __init__(self) -> None:
        super().__init__(None)
        self.setupUi(self)  # type:ignore
        self.vm = UserViewModel()

        self.initialize_bindings()

    def initialize_bindings(self) -> None:
        self.vm.user.bind(self._bind_handler)
        self.binding_lineedit(
            self.entryName, self.vm.user.bindable("name", str), bindings="on-typing"
        )
        self.binding_spinbox(self.spinAge, self.vm.user.bindable("age", int))
        self.binding_command(self.buttonDisplay, self.vm.command_display_user)
        return None

    def _bind_handler(self, name: str, value: object): ...
