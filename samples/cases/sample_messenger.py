# coding:utf-8
from typing import Any

from qtpy.QtCore import QCoreApplication

from qtmvvmtoolkit.messenger import Message, Messenger


class IntMessage(Message[int]):
    pass


class StrMessage(Message[str]):
    pass


def operation(value: Any):
    print(f"value->{value}")
    return None


def s_operation(value: Any):
    print(f"()value()->{value}()")
    return None


def main() -> None:
    app = QCoreApplication([])

    Messenger.Default.register(IntMessage)
    Messenger.Default.register(StrMessage)

    Messenger.Default.use(IntMessage, operation)
    Messenger.Default.use(IntMessage, s_operation)
    Messenger.Default.use(StrMessage, operation)
    Messenger.Default.use(StrMessage, s_operation)

    Messenger.Default.send(IntMessage(6))
    Messenger.Default.send(StrMessage("sdfdsfdsf===>"))
    app.exec()
    return None


if __name__ == "__main__":
    main()
