# coding:utf-8
import typing

from context import register_package

register_package()
from qtmvvmtoolkit.inputs import observable_object


def handle_changes(name: str, value: typing.Any) -> None:
    print(f"name:{name} & value:{value}")
    return


@observable_object
class User:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age
        return


def main() -> None:
    from PyQt6.QtWidgets import QApplication, QLineEdit, QPushButton

    user = User("viktor", 26)

    def btn_slot():
        print(user.get_attributes())
        return

    app = QApplication([])
    line = QLineEdit()
    button = QPushButton("Check Info")
    user.name.binding(line.setText)
    user.name.rbinding(line.textChanged)
    user.name.binding(lambda v: print(f"changed -> {v}"))
    # user.name.set("c")
    button.clicked.connect(btn_slot)
    line.show()
    button.show()
    app.exec()
    return


main()
