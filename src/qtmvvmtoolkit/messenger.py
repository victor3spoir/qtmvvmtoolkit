# coding:utf-8
import typing
from typing import Any, Callable, Generic, TypeVar

from events import Event
from qtpy.QtCore import QObject, Signal

FuncT = typing.TypeVar("FuncT", bound=typing.Callable)


T = TypeVar("T")


class SigInst(Generic[T]):
    @staticmethod
    def connect(slot: Callable[[T], typing.Any], type: type | None = None) -> None: ...

    @staticmethod
    def disconnect(slot: Callable[[T], typing.Any] = typing.Any) -> None: ...

    @staticmethod
    def emit(*args: T) -> None: ...


class WorkerBaseSignals(QObject):
    message = Signal(object)  # emitted when the work is started


class Message(QObject, Generic[T]):
    message: SigInst[T]

    def __init__(self, value: T) -> None:
        super().__init__(None)
        self._value = value
        self.signals = WorkerBaseSignals()
        return

    def __getattr__(self, name: str) -> SigInst:
        attr = getattr(self.signals.__class__, name, None)
        if isinstance(attr, Signal):
            return getattr(self.signals, name)
        raise AttributeError(
            f"{self.__class__.__name__!r} object has no attribute {name!r}"
        )

    @property
    def value(self) -> T:
        return self._value

    @classmethod
    def name(cls) -> str:
        return cls.__name__

    def send(self) -> None:
        self.message.emit(self._value)
        return None

    def register(self, func: Callable[[T], typing.Any]) -> None:
        self.message.connect(func)
        return None

    def unregister(self, func: Callable[[T], typing.Any]) -> None:
        try:
            self.message.disconnect(func)
        except TypeError as ex:
            print("this function is not connected")
            raise ex
        return None


class Messenger:
    """_summary_

    Raises:
        AttributeError: _description_
        Exception: _description_

    Returns:
        _type_: _description_
    """

    # _Default: typing.Any

    def __init__(self) -> None:
        self._messages: typing.Dict[
            str, typing.List[typing.Callable[[], typing.Any]]
        ] = dict()
        return

    @classmethod
    @property
    def Default(cls):
        try:
            return Messenger._Default
        except AttributeError:
            Messenger._Default = Messenger()
            return Messenger._Default

    def register(self, message: typing.Type[Message[Any]]) -> None:
        if message.__name__ not in self._messages.keys():
            self._messages.update({message.__name__: []})
        return None

    def use(self, message: typing.Type[Message[Any]], func: Callable[[T], Any]):
        if message.__name__ not in self._messages.keys():
            raise Exception(f"Message:{message.__name__}  doesn't exists")

        value: typing.List[typing.Any] = self._messages.get(message.__name__)
        if func in value:
            return None
        value.append(func)
        self._messages.update({message.__name__: value})
        return None

    def unuse(self, message: typing.Type[Message[Any]], func: Callable[[T], Any]):
        if message.__name__ in self._messages.keys():
            _funcs = self._messages.get(message.__name__)
            if func in _funcs:
                _funcs.remove(func)
            self._messages.update({message.__name__: _funcs})
        else:
            print("Message dont exists")
        return None

    def send(self, message: Message[Any]) -> None:
        _exists = message.__class__.__name__ in self._messages
        if _exists:
            _funcs = self._messages.get(message.__class__.__name__)
            for func in _funcs:
                message.register(func)
                message.send()
                message.unregister(func)
        return None


# T = typing.TypeVar("T")


class MessageV2(typing.Generic[T]):
    def __init__(self, data: T) -> None:
        super().__init__()
        self._data = data
        self.changed = Event[T]()
        return

    def register(self, func: typing.Callable[[T], None]):
        self.changed += func
        return

    def throw(self) -> None:
        self.changed(self._data)
        return


class MessengerV2:
    _default: "MessengerV2" = None  # type:ignore

    @classmethod
    def Default(cls) -> "MessengerV2":
        cls._default = cls._default or MessengerV2()
        return cls._default

    def __init__(self) -> None:
        self.messages: typing.Dict[
            str, typing.List[typing.Callable[[typing.Any], None]]
        ] = {}
        return

    def register(
        self,
        message: typing.Type[MessageV2[T]],
        func: typing.Callable[[T], None],
    ) -> None:
        if message.__name__ not in self.messages:
            self.messages.update({message.__name__: []})
        _functions = self.messages.get(message.__name__, [])
        if func not in _functions:
            _functions.append(func)
        self.messages.update({message.__name__: _functions})
        return None

    def unregister(
        self,
        message: typing.Type[MessageV2[T]],
        func: typing.Callable[[T], None],
    ) -> None:
        if message.__name__ not in self.messages:
            self.messages.update({message.__name__: []})
        _functions = self.messages.get(message.__name__, [])
        if func in _functions:
            _functions.remove(func)
        self.messages.update({message.__name__: _functions})
        return None

    def send(self, message: MessageV2[typing.Any]) -> None:
        if message.__class__.__name__ in self.messages:
            for function in self.messages.get(message.__class__.__name__, []):
                message.changed += function
                message.throw()
                message.changed -= function
        return None
