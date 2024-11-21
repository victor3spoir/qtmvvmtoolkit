# coding:utf-8
import context

context.__file__

import sys

from PyQt6.QtWidgets import *
from qtmvvmtoolkit.inputs import ObservableProperty
from qtmvvmtoolkit.objects import BindableObject


class SimpleDataBindingViewModel:
    def __init__(self) -> None:
        self.username = ObservableProperty[str]("")
        self.email = ObservableProperty[str]("")
        self.age = ObservableProperty[int](0)
        self.confirm = ObservableProperty[bool](False)
        return


class SimpleDataBindingWidget(QWidget, BindableObject):
    def __init__(self, vm: SimpleDataBindingViewModel):
        super().__init__()
        self.vm = vm

        self.initialize_components()
        self.initialize_bindings()
        pass

    def initialize_components(self) -> None:
        layout = QFormLayout(self)
        layout.addWidget(QLabel("<h1>Simple Application</h1>"))

        self.lineedit_username = QLineEdit()
        self.lineedit_email = QLineEdit()
        self.spin_age = QSpinBox()
        self.check_confirm = QCheckBox()

        self.label_username = QLabel("-")
        self.label_email = QLabel("-")
        self.label_age = QLabel("-")
        self.label_confirm = QLabel("-")

        layout.addRow("Username", self.lineedit_username)
        layout.addRow("Email", self.lineedit_email)
        layout.addRow("Age", self.spin_age)
        layout.addRow("Confirm", self.check_confirm)
        #
        layout.addWidget(QLabel("<h2>Binding data to Label to see changings</h2>"))
        layout.addWidget(self.label_username)
        layout.addWidget(self.label_email)
        layout.addWidget(self.label_age)
        layout.addWidget(self.label_confirm)
        return

    def initialize_bindings(self) -> None:
        self.binding_value(
            self.lineedit_username,
            self.vm.username,
            bindings="on-typed",
        )
        self.binding_value(self.lineedit_email, self.vm.email, bindings="on-typed")
        self.binding_value(self.spin_age, self.vm.age)
        self.binding_value(self.check_confirm, self.vm.confirm)
        #
        self.binding_value(
            self.label_username, self.vm.username, string_format="{} (new user)"
        )
        self.binding_value(self.label_email, self.vm.email)
        self.binding_value(self.label_age, self.vm.age)
        self.binding_value(self.label_confirm, self.vm.confirm)
        return


app = QApplication(sys.argv)
w = SimpleDataBindingWidget(SimpleDataBindingViewModel())
w.show()
w.setFocus()
app.exec()
