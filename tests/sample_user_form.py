# coding:utf-8
import sys

import context
from qtmvvmtoolkit.inputs import ObservableProperty
from qtmvvmtoolkit.objects import QtBindableObject

context.__file__
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QSpinBox,
    QLabel,
    QApplication,
)


class ViewModel:
    def __init__(self) -> None:
        self.username = ObservableProperty[str]("")
        self.email = ObservableProperty[str]("")
        self.age = ObservableProperty[int](10)


class Widget(QWidget, QtBindableObject):
    def __init__(self, vm: ViewModel, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._vm = vm

        layout = QVBoxLayout(self)

        self.line_username = QLineEdit()
        self.line_email = QLineEdit()
        self.spin_age = QSpinBox()

        layout.addWidget(QLabel("Username"))
        layout.addWidget(self.line_username)
        layout.addWidget(QLabel("Email"))
        layout.addWidget(self.line_email)
        layout.addWidget(QLabel("Age"))
        layout.addWidget(self.spin_age)

        layout.addWidget(QLabel("<h2>Watch</h2>"))
        self.label_username = QLabel("---")
        self.label_email = QLabel("---")
        self.label_age = QLabel("---")
        layout.addWidget(self.label_username)
        layout.addWidget(self.label_email)
        layout.addWidget(self.label_age)

        self.initialize_bindings()
        ...

    def initialize_bindings(self) -> None:
        self.binding_lineedit(self.line_username, self._vm.username)
        self.binding_lineedit(self.line_email, self._vm.email)
        self.binding_spinbox(self.spin_age, self._vm.age)

        self.binding_label(self.label_username, self._vm.username)
        self.binding_label(self.label_email, self._vm.email)
        self.binding_label(self.label_age, self._vm.age)
        return None


if __name__ == "__main__":
    app = QApplication([])
    w = Widget(ViewModel())
    w.show()
    sys.exit(app.exec())
