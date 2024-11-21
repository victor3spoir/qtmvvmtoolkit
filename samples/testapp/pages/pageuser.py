# coding:utf-8
from pages.templates.PageUser_ui import Ui_PageUser
from qtmvvmtoolkit.objects import BindableObject
from qtpy.QtWidgets import QWidget
from viewmodels.uservm import UserViewModel


class PageUser(QWidget, Ui_PageUser, BindableObject):
    def __init__(self) -> None:
        super().__init__(None)
        self.setupUi(self)  # type:ignore
        self.vm = UserViewModel()

        self.initialize_bindings()
        return

    def initialize_bindings(self) -> None:
        print(f":::binding {self.vm.user}")
        self.binding_value(self.entryName, self.vm.user.name, bindings="on-typing")
        self.binding_value(self.spinAge, self.vm.user.age)
        self.binding_command(self.buttonDisplay, self.vm.command_display_user)
        return None
