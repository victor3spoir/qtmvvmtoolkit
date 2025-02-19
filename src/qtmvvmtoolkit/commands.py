# -*- coding:utf-8 -*-
import typing
from typing import Any, Callable

from qtpy.QtCore import Slot


@Slot()
class RelayCommand:
    """Relay command for button"""

    @typing.overload
    def __init__(self, func: Callable[..., None]) -> None: ...

    @typing.overload
    def __init__(
        self, func: Callable[..., None], **kwargs: dict[typing.Any, typing.Any]
    ) -> None: ...

    def __init__(
        self, func: Callable[..., None], **kwargs: dict[typing.Any, typing.Any]
    ) -> None:
        self.func = func
        self.kwargs = kwargs
        return None

    def __call__(self) -> Any:
        if self.kwargs:
            return self.func(**self.kwargs)
        return self.func()


@Slot()
class RCommand:
    @typing.overload
    def __init__(self, func: Callable[..., None]) -> None: ...

    @typing.overload
    def __init__(
        self, func: Callable[..., None], **kwargs: dict[typing.Any, typing.Any]
    ) -> None: ...

    def __init__(
        self, func: typing.Callable[..., None], **kwargs: dict[typing.Any, typing.Any]
    ) -> None:
        self.func = func
        self.is_running: bool = False
        self.kwargs = kwargs
        return

    def execute(self, *args: Any, **kwargs: Any) -> None:
        self.is_running = True
        self.func(*args, **self.kwargs)
        self.is_running = False
        return

    def can_execute(self) -> bool:
        return not self.is_running

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        if not self.can_execute():
            return
        return self.execute(*args, **kwargs)


def rcommand(**kwargs: Any):
    def rcommand_inner(func: typing.Callable[..., None]):
        command = RCommand(func, **kwargs)
        return command

    return rcommand_inner
