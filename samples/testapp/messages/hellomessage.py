from qtmvvmtoolkit.messenger import MessageV2


class HelloMessage(MessageV2[str]): ...


class StateChangedMessage(MessageV2[bool]): ...
