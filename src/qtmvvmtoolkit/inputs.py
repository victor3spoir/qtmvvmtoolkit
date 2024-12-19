# coding:utf-8
import typing
from typing import Generic, TypeVar
import warnings


from loguru import logger
from qtpy.QtCore import Signal
from qtpy.QtWidgets import QComboBox
from events import Event


_T = TypeVar("_T")
T = TypeVar("T")


class ObservableProperty(Generic[_T]):
    def __init__(self, value: _T):
        super().__init__()
        self.valueChanged = Event[_T]()
        self._type = type(value)
        self.value: _T = value
        self.set(value)
        # self.signals = ObservableSignals()
        return

    def get(self) -> _T:
        return self.value

    def set(self, value: _T):
        if not isinstance(value, (self._type)):
            logger.warning(
                f"The type of value {type(value)} is incompatible with {self._type}"
            )
            return
        if value != self.value:
            self.value = value
            self.valueChanged(self.value)
        return

    def binding(self, method: typing.Callable[..., None]) -> None:
        """One way binding"""
        self.valueChanged += method
        self.valueChanged(self.get())
        return None

    def rbinding(self, signal: Signal) -> None:
        """Reverse binding method"""
        signal.connect(lambda v: self.set(v))
        self.valueChanged(self.get())
        return None


class ComputedObservableProperty(Generic[_T]):
    def __init__(
        self,
        value: _T,
        observable_props: typing.List[ObservableProperty[_T]],
        update_function: typing.Callable[..., _T],
    ) -> None:
        super().__init__()
        self.valueChanged = Event[_T]()
        self.value: _T = value
        self.update_function = update_function
        self.observable_props = observable_props

        for observable_prop in self.observable_props:
            observable_prop.valueChanged += self.update
        return

    def get(self) -> _T:
        return self.value

    def set(self, value: _T):
        self.value = value
        self.valueChanged(self.value)
        return None

    def update(self, value: _T) -> None:
        _result = self.update_function()
        self.set(_result)
        return None

    def binding(self, method: typing.Callable[..., None]) -> None:
        """One way binding"""
        self.valueChanged += method
        self.valueChanged(self.get())
        return None


class ObservableCollection(typing.Generic[_T]):
    def __init__(self, collection: list[_T]) -> None:
        super().__init__()
        self.valueChanged = Event[typing.List[_T]]()
        self.collection = collection
        return None

    def get(self) -> list[_T]:
        return self.collection

    def set(self, collection: list[_T]) -> None:
        self.collection = collection
        self.valueChanged(collection)
        return None

    def clear(self) -> None:
        self.collection.clear()
        self.valueChanged(self.collection)
        return None

    def append(self, value: _T) -> None:
        self.collection.append(value)
        self.valueChanged(self.collection)
        return None

    def remove(self, data: _T) -> None:
        self.collection.remove(data)
        self.valueChanged(self.collection)
        return None

    def extend(self, collection: list[_T]) -> None:
        self.collection.extend(collection)
        self.valueChanged(self.collection)
        return None

    def pop(self, index: int) -> _T:
        _poped = self.collection.pop(index)
        self.valueChanged(self.collection)

        return _poped

    def binding(self, method: typing.Callable[[typing.Any], None]) -> None:
        """One way binding"""
        self.valueChanged += method
        self.valueChanged(self.get())
        return None

    def bind_combobox(self, widget: QComboBox):
        widget.clear()
        self.valueChanged += lambda v: widget.addItems(v)
        self.valueChanged(self.collection)
        return None

    def __getitem__(self, index: int) -> _T:
        return self.collection[index]

    def __len__(self) -> int:
        return len(self.collection)

    def __contains__(self, item: _T) -> bool:
        return item in self.collection

    def __iter__(self) -> typing.Iterator[_T]:
        return iter(self.collection)


class IObservableObject:
    def get_attribute(self) -> typing.Dict[str, typing.Any]:
        return {k: v.get() for k, v in self.__dict__.items()}

    def set_attribute(self, data: typing.Dict[str, typing.Any]) -> None:
        for k, v in self.__dict__.items():
            if k in data:
                v.set(data.get(k))
        return None


def observable_object(target_class: typing.Type[IObservableObject]):
    # def wrapper(*args: typing.List[typing.Any], **kwargs: typing.Dict[str, typing.Any]):
    warnings.warn(
        "WARN: this is preview feature & should in instable & change in future"
    )

    # create custom function to retrieve basic attribute
    # def get_attribute(self) -> typing.Dict[str, typing.Any]:
    #     return {k: v.get() for k, v in self.__dict__.items()}

    # target_class.get_attribute = get_attribute

    def wrapper(*args: typing.List[typing.Any], **kwargs: typing.Dict[str, typing.Any]):
        instance = target_class(*args, **kwargs)
        for k, v in instance.__dict__.items():
            setattr(instance, k, ObservableProperty[type(v)](v))
        return instance

    return wrapper
