# coding:utf-8
# import typing
# from typing import TypeVar

# from events import Event

# FuncT = typing.TypeVar("FuncT", bound=typing.Callable)


# T = TypeVar("T")


# class MessageV2(typing.Generic[T]):
#     def __init__(self, data: T) -> None:
#         super().__init__()
#         self._data = data
#         self.changed = Event[T]()
#         return None

#     def register(self, func: typing.Callable[[T], None]):
#         self.changed += func
#         return None

#     def throw(self) -> None:
#         self.changed(self._data)
#         return None


# class MessengerV2:
#     _default: "MessengerV2" = None  # type:ignore

#     @classmethod
#     def default(cls) -> "MessengerV2":
#         cls._default = cls._default or MessengerV2()
#         return cls._default

#     def __init__(self) -> None:
#         self.messages: typing.Dict[
#             str, typing.List[typing.Callable[[typing.Any], None]]
#         ] = {}
#         return None

#     def register(
#         self,
#         message: typing.Type[MessageV2[T]],
#         func: typing.Callable[[T], None],
#     ) -> None:
#         if message.__name__ not in self.messages:
#             self.messages.update({message.__name__: []})
#         _functions = self.messages.get(message.__name__, [])
#         if func not in _functions:
#             _functions.append(func)
#         self.messages.update({message.__name__: _functions})
#         return None

#     def unregister(
#         self,
#         message: typing.Type[MessageV2[T]],
#         func: typing.Callable[[T], None],
#     ) -> None:
#         if message.__name__ not in self.messages:
#             self.messages.update({message.__name__: []})
#         _functions = self.messages.get(message.__name__, [])
#         if func in _functions:
#             _functions.remove(func)
#         self.messages.update({message.__name__: _functions})
#         return None

#     def send(self, message: MessageV2[typing.Any]) -> None:
#         if message.__class__.__name__ in self.messages:
#             for function in self.messages.get(message.__class__.__name__, []):
#                 message.changed += function
#                 message.throw()
#                 message.changed -= function
#         return None


import typing
from collections import defaultdict
from typing import Any, Callable, Dict, List, TypeVar

from events import Event

T = TypeVar("T")


class Message(typing.Generic[T]):
    def __init__(self, data: T) -> None:
        super().__init__()
        self._data = data
        self.changed = Event[T]()

    def register(self, func: Callable[[T], None]) -> None:
        self.changed += func

    def throw(self) -> None:
        self.changed(self._data)


class Messenger:
    _default: "Messenger" = None  # type:ignore

    @classmethod
    def default(cls) -> "Messenger":
        if cls._default is None:
            cls._default = Messenger()
        return cls._default

    def __init__(self) -> None:
        self.messages: Dict[str, List[Callable[[Any], None]]] = defaultdict(list)

    def register(
        self,
        message: typing.Type[Message[T]],
        func: Callable[[T], None],
    ) -> None:
        if func not in self.messages[message.__name__]:
            self.messages[message.__name__].append(func)

    def unregister(
        self,
        message: typing.Type[Message[T]],
        func: Callable[[T], None],
    ) -> None:
        if func in self.messages[message.__name__]:
            self.messages[message.__name__].remove(func)

    def send(self, message: Message[Any]) -> None:
        for function in self.messages.get(message.__class__.__name__, []):
            function(message._data)
