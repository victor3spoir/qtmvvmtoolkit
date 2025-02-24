# coding:utf-8
import typing
from typing import Generic, TypeVar
import warnings

from loguru import logger
from qtpy.QtCore import Signal
from qtpy.QtWidgets import QComboBox
from events import Event
import dataclasses


_T = TypeVar("_T")
T = TypeVar("T")


class ObservableProperty(Generic[_T]):
    def __init__(self, value: _T):
        super().__init__()
        self.valueChanged = Event[_T]()
        self._type = type(value)
        self.value: _T = value
        self.set(value)
        ...

    def get(self) -> _T:
        return self.value

    def set(self, value: _T):
        if not isinstance(value, (self._type)):
            logger.warning(
                f"The type of value {type(value)} is incompatible with {self._type}"
            )
            return None
        if value != self.value:
            self.value = value
            self.valueChanged(self.value)
        return None

    def binding(self, method: typing.Callable[..., None]) -> None:
        """One way binding"""
        self.valueChanged += method
        self.valueChanged(self.get())
        return None

    def rbinding(self, signal: Signal) -> None:
        """Reverse binding method"""
        signal.connect(self.set)
        self.valueChanged(self.get())
        return None


class ComputedObservableProperty(Generic[_T]):
    def __init__(
        self,
        value: _T,
        observable_props: typing.List[ObservableProperty[typing.Any]],
        update_function: typing.Callable[..., _T],
    ) -> None:
        super().__init__()
        self.valueChanged = Event[_T]()
        self.value: _T = value
        self.update_function = update_function
        self.observable_props = observable_props

        for observable_prop in self.observable_props:
            observable_prop.valueChanged += self.update
        return None

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


# class IObservableObject:
#     def get_attribute(self) -> typing.Dict[str, typing.Any]:
#         return {k: v.get() for k, v in self.__dict__.items()}

#     def set_attribute(self, data: typing.Dict[str, typing.Any]) -> None:
#         for k, v in self.__dict__.items():
#             if k in data:
#                 v.set(data.get(k))
#         return None


# def observable_object(target_class: typing.Type[IObservableObject]):
#     # def wrapper(*args: typing.List[typing.Any], **kwargs: typing.Dict[str, typing.Any]):
#     warnings.warn(
#         "WARN: this is preview feature & should in instable & change in future"
#     )

#     # create custom function to retrieve basic attribute
#     # def get_attribute(self) -> typing.Dict[str, typing.Any]:
#     #     return {k: v.get() for k, v in self.__dict__.items()}

#     # target_class.get_attribute = get_attribute

#     def wrapper(*args: typing.List[typing.Any], **kwargs: typing.Dict[str, typing.Any]):
#         instance = target_class(*args, **kwargs)
#         for k, v in instance.__dict__.items():
#             setattr(instance, k, ObservableProperty[type(v)](v))
#         return instance

#     return wrapper


# @dataclasses.dataclass
# class ObservableClass:
#     _value_changed: Event[str, object] = dataclasses.field(
#         default_factory=lambda: Event[str, object]()
#     )
#     _bindables: typing.Dict[str, ObservableProperty[typing.Any]] = dataclasses.field(
#         default_factory=lambda: {}
#     )

#     def __post_init__(self):
#         logger.debug("Start create bindables properties at post_init")
#         for key, value in self.__dict__.items():
#             # not isinstance(
#             #     getattr(self, key, None), (Event, ObservableProperty)
#             # ) or
#             if key.lower() not in ["_value_changed", "_bindables"]:
#                 self._bindables.update(
#                     {f"bindable_{key}": ObservableProperty[type(key)](value)}
#                 )
#                 try:
#                     self._bindables.get(f"bindable_{key}").valueChanged += (
#                         lambda v: print(
#                             f"changing...{self._bindables.get(f'bindable_{key}').get()}"
#                         )
#                     )
#                     # self._bindables.get(f"bindable_{key}").binding(
#                     #     # lambda v: print(f"changing...{v}")
#                     #     lambda v: setattr(self, key, value)
#                     # )
#                     self._bindables.get(f"bindable_{key}").set(value)
#                 except AttributeError as ex:
#                     logger.exception(
#                         f"Error occurs while bindable created bindables properties, {ex}"
#                     )
#                     pass
#         return None

#     def bindable(self, name: str, item: typing.Type[T]) -> ObservableProperty[T]:
#         if _bindable := self._bindables.get(f"bindable_{name}"):
#             # if not _bindable:
#             logger.warning(f"No observable found for {name}")
#             logger.debug(
#                 f"Observable found for {name}:{_bindable}",
#             )
#         return _bindable
#         ...

#     def bind(self, handler: typing.Callable[[str, object], None]):
#         self._value_changed += handler
#         return None

#     def rbind(self, event: Event[str, object]):
#         event += self._apply_reverse_changes
#         return None

#     def _apply_reverse_changes(self, name: str, value: typing.Any) -> None:
#         if name in [field.name for field in dataclasses.fields(self)]:
#             if isinstance(value, type(getattr(self, name))):
#                 setattr(self, name, value)
#                 pass
#             else:
#                 print(f"Incompatible type provided for {name}")
#             pass
#         return None

#     def __setattr__(self, name: str, value: typing.Any) -> None:
#         # Update simple attr
#         if not isinstance(getattr(self, name, None), (Event, ObservableProperty)):
#             super().__setattr__(name, value)
#             self._value_changed(name, value)
#             try:
#                 self.__update_observable_on_attribute_updated(name, value)
#             except Exception as ex:
#                 logger.exception(f"Bindable property for {name} not found, {ex}")
#             return None
#         # if isinstance(getattr(self, name, None), (ObservableClass)):
#         #     print("update observable///")
#         logger.debug(f"Setting Events & Observables variable {name} with {value}")
#         print("unreachable reached")
#         return None

#     def __update_observable_on_attribute_updated(self, name: str, value: typing.Any):
#         self._bindables.get(f"bindable_{name}").set(value)
#         return

#     def to_dict(self) -> typing.Dict[str, object]:
#         _dict = {
#             key: value
#             for key, value in self.__dict__.items()
#             if key not in ["_value_changed", "_bindables"]
#         }
#         return _dict


# @dataclasses.dataclass
# class ObservableClassV2:
#     _value_changed: Event[str, object] = dataclasses.field(
#         default_factory=lambda: Event[str, object]()
#     )
#     _bindables: typing.Dict[str, ObservableProperty[typing.Any]] = dataclasses.field(
#         default_factory=lambda: {}
#     )

#     def __post_init__(self):
#         logger.debug("Start creating bindable properties at post_init")

#         # Create bindable properties for each attribute
#         for key, value in self.__dict__.items():
#             if key.lower() not in ["_value_changed", "_bindables"]:
#                 bindable_key = f"bindable_{key}"
#                 if bindable_key not in self._bindables:
#                     self._bindables[bindable_key] = ObservableProperty(value)
#                 else:
#                     logger.warning(f"Bindable already exists for {key}. Skipping...")
#                 self._bindables[bindable_key].binding(self._on_bindable_changed)

#         return None

#     def bindable(self, name: str) -> ObservableProperty[typing.Any]:
#         # Get the bindable by its name
#         bindable_key = f"bindable_{name}"
#         if bindable_key not in self._bindables:
#             logger.warning(f"No observable found for {name}")
#         return self._bindables.get(bindable_key, None)

#     def _on_bindable_changed(self, value: typing.Any) -> None:
#         # Update attribute when the bindable value changes
#         for key, bindable in self._bindables.items():
#             if bindable.get() != value:
#                 attribute_name = key.replace("bindable_", "")
#                 setattr(self, attribute_name, value)
#                 break  # Stop at the first change (or handle multiple if necessary)
#         return None

#     def bind(self, handler: typing.Callable[[str, object], None]):
#         # Binding function for external observers
#         self._value_changed += handler

#     def rbind(self, event: Event[str, object]):
#         # Reverse binding event
#         event += self._apply_reverse_changes

#     def _apply_reverse_changes(self, name: str, value: typing.Any) -> None:
#         # Apply reverse changes from external events
#         if name in [field.name for field in dataclasses.fields(self)]:
#             if isinstance(value, type(getattr(self, name))):
#                 setattr(self, name, value)
#             else:
#                 logger.warning(f"Incompatible type provided for {name}")
#         return None

#     def __setattr__(self, name: str, value: typing.Any) -> None:
#         # Update simple attributes and bindable attributes
#         if name not in ["_value_changed", "_bindables"]:
#             if name.startswith("bindable_"):
#                 # Set observable property
#                 bindable_name = name.replace("bindable_", "")
#                 if bindable_name in self._bindables:
#                     self._bindables[name].set(value)
#             else:
#                 super().__setattr__(name, value)
#                 self._value_changed(name, value)

#     def to_dict(self) -> typing.Dict[str, object]:
#         # Convert the class to a dictionary
#         return {
#             key: value
#             for key, value in self.__dict__.items()
#             if key not in ["_value_changed", "_bindables"]
#         }
