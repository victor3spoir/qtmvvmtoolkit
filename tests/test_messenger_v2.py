# coding:utf-8


import context
from qtmvvmtoolkit.messenger import Message, Messenger

context.__file__


class StrMessage(Message[str]): ...


class IntMessage(Message[str]): ...


def called_from(value: str):
    print(f"{value}")
    return None


class TestMessengerV2:
    def test_message_case(self):
        messenger = Messenger()
        messenger.register(StrMessage, lambda v: print(f"messenger:send {v}"))
        messenger.register(StrMessage, called_from)

        messenger.send(StrMessage("some-data"))
        print("///\n")
        messenger.unregister(StrMessage, called_from)
        messenger.send(StrMessage("second-data"))

        assert 1 == 1
        return
