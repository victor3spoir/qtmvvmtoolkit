# coding:utf-8


import context
from qtmvvmtoolkit.messenger import MessageV2, MessengerV2

context.__file__


class StrMessage(MessageV2[str]): ...


class IntMessage(MessageV2[str]): ...


def called_from(value: str):
    print(f"{value}")
    return None


class TestMessengerV2:
    def test_message_case(self):
        messenger = MessengerV2()
        messenger.register(StrMessage, lambda v: print(f"messenger:send {v}"))
        messenger.register(StrMessage, called_from)

        messenger.send(StrMessage("some-data"))
        print("///\n")
        messenger.unregister(StrMessage, called_from)
        messenger.send(StrMessage("second-data"))

        assert 1 == 1
        return
