# coding:utf-8
from datetime import date
import sys

import context
from qtmvvmtoolkit.inputs import ObservableProperty
from qtmvvmtoolkit.objects import BindableObject

context.__file__
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QSpinBox,
    QLabel,
    QCheckBox,
    QApplication,
    QDateEdit,
)


class ViewModel:
    def __init__(self) -> None:
        self.username = ObservableProperty[str]("john doe")
        self.email = ObservableProperty[str]("john@doe.de")
        self.age = ObservableProperty[int](10)
        self.birthdate = ObservableProperty[date](date.today())
        self.is_visible = ObservableProperty[bool](True)


class Widget(QWidget, BindableObject):
    def __init__(self, vm: ViewModel, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._vm = vm

        layout = QVBoxLayout(self)

        self.line_username = QLineEdit()
        self.line_email = QLineEdit()
        self.spin_age = QSpinBox()
        self.check_visible = QCheckBox()
        self.date_birthdate = QDateEdit()

        layout.addWidget(QLabel("Username"))
        layout.addWidget(self.line_username)
        layout.addWidget(QLabel("Email"))
        layout.addWidget(self.line_email)
        layout.addWidget(QLabel("Age"))
        layout.addWidget(self.spin_age)
        layout.addWidget(QLabel("Visible"))
        layout.addWidget(self.check_visible)
        layout.addWidget(QLabel("BirthDate"))
        layout.addWidget(self.date_birthdate)

        layout.addWidget(QLabel("<h2>Watch</h2>"))
        self.label_username = QLabel("---")
        self.label_email = QLabel("---")
        self.label_age = QLabel("---")
        self.label_birthdate = QLabel("---")
        self.label_visible = QLabel("IsVisisble or Not")
        layout.addWidget(self.label_username)
        layout.addWidget(self.label_email)
        layout.addWidget(self.label_age)
        layout.addWidget(self.label_visible)
        layout.addWidget(self.label_birthdate)

        self.initialize_bindings()
        ...

    def initialize_bindings(self) -> None:
        self.binding_lineedit(self.line_username, self._vm.username)
        self.binding_lineedit(self.line_email, self._vm.email)
        self.binding_spinbox(self.spin_age, self._vm.age)
        self.binding_checkbox(self.check_visible, self._vm.is_visible)
        self.binding_dateedit(self.date_birthdate, self._vm.birthdate)

        self.binding_label(self.label_username, self._vm.username)
        self.binding_label(self.label_email, self._vm.email)
        self.binding_label(self.label_age, self._vm.age)
        # self.binding_state(self.label_visible, self._vm.is_visible, "visibility")
        self.binding_label(self.label_visible, self._vm.is_visible)
        self.binding_label(self.label_birthdate, self._vm.birthdate)
        return None


if __name__ == "__main__":
    from qdarktheme import load_palette, load_stylesheet

    app = QApplication([])
    app.setStyleSheet(load_stylesheet("auto"))
    app.setPalette(load_palette("auto"))
    w = Widget(ViewModel())
    w.show()
    sys.exit(app.exec())
