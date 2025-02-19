# coding:utf-8
from typing import Any

from qtmvvmtoolkit.messenger import Message, Messenger
from qtpy.QtCore import QCoreApplication


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
    Messenger.default().register(IntMessage, operation)
    Messenger.default().register(IntMessage, s_operation)
    Messenger.default().register(StrMessage, operation)
    Messenger.default().register(StrMessage, s_operation)

    # MessengerV2.Default.use(IntMessage, operation)

    Messenger.default().send(IntMessage(6))
    Messenger.default().send(StrMessage("sdfdsfdsf===>"))
    app.exec()
    return None


if __name__ == "__main__":
    main()
