# coding:utf-8
import random
import sys

import context
from qtmvvmtoolkit.commands import RelayCommand
from qtmvvmtoolkit.inputs import ObservableCollection, ObservableProperty
from qtmvvmtoolkit.objects import BindableObject

context.__file__
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QSpinBox,
    QLabel,
    QApplication,
    QComboBox,
    QPushButton,
)


class ViewModel:
    def __init__(self) -> None:
        self.username = ObservableProperty[str]("john doe")
        self.email = ObservableProperty[str]("john@doe.de")
        self.age = ObservableProperty[int](18)
        self.roles = ObservableCollection[str](["admin", "user", "guest"])
        self.selected_role = ObservableProperty[str]("")

    def update_roles(self) -> None:
        self.roles.append(f"role-{random.randint(1, 100)}")
        return None


class Widget(QWidget, BindableObject):
    def __init__(self, vm: ViewModel, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._vm = vm

        layout = QVBoxLayout(self)

        self.line_username = QLineEdit()
        self.line_email = QLineEdit()
        self.spin_age = QSpinBox()
        self.cbox_roles = QComboBox()
        self.button_update = QPushButton("Update")

        layout.addWidget(QLabel("Username"))
        layout.addWidget(self.line_username)
        layout.addWidget(QLabel("Email"))
        layout.addWidget(self.line_email)
        layout.addWidget(QLabel("Age"))
        layout.addWidget(self.spin_age)
        layout.addWidget(QLabel("Roles"))
        layout.addWidget(self.cbox_roles)
        layout.addWidget(QLabel("Update command"))
        layout.addWidget(self.button_update)

        layout.addWidget(QLabel("<h2>Watch</h2>"))
        self.label_username = QLabel("---")
        self.label_email = QLabel("---")
        self.label_age = QLabel("---")
        self.label_role = QLabel("---")
        layout.addWidget(self.label_username)
        layout.addWidget(self.label_email)
        layout.addWidget(self.label_age)
        layout.addWidget(self.label_role)

        self.initialize_bindings()
        ...

    def initialize_bindings(self) -> None:
        self.binding_lineedit(self.line_username, self._vm.username)
        self.binding_lineedit(self.line_email, self._vm.email)
        self.binding_spinbox(self.spin_age, self._vm.age)
        self.binding_selection(
            self.cbox_roles,
            self._vm.roles,
            default_select=True,
            observable_value=self._vm.selected_role,
        )
        self.binding_command(self.button_update, RelayCommand(self._vm.update_roles))

        self.binding_label(self.label_username, self._vm.username)
        self.binding_label(self.label_email, self._vm.email)
        self.binding_label(self.label_age, self._vm.age)
        self.binding_label(self.label_role, self._vm.selected_role)
        return None


if __name__ == "__main__":
    from qdarktheme import load_stylesheet, load_palette

    app = QApplication([])
    app.setStyleSheet(load_stylesheet("auto"))
    app.setPalette(load_palette("auto"))
    w = Widget(ViewModel())
    w.show()
    sys.exit(app.exec())
