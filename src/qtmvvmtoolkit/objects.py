# coding:utf-8

import typing
import warnings
from datetime import date, datetime

from qtpy.QtCore import QDate, QDateTime, QObject, QVariant
from qtpy.QtGui import QAction
from qtpy.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDoubleSpinBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QSpinBox,
    QTextEdit,
    QToolButton,
    QWidget,
)

from qtmvvmtoolkit.commands import RCommand, RelayCommand
from qtmvvmtoolkit.converters import IValueConverter
from qtmvvmtoolkit.inputs import (
    ComputedObservableProperty,
    ObservableCollection,
    ObservableProperty,
)

T = typing.TypeVar("T")


class ObservableObject:
    def observables_data(self) -> typing.Dict[str, typing.Any]: ...


class BindableObject(QObject):
    def __init__(
        self,
        parent: typing.Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        ...

    def initialize_components(self) -> None:
        raise NotImplementedError(
            "Please, redefine this function, and call it in the init"
        )

    def initialize_bindings(self) -> None:
        raise NotImplementedError(
            "Please, redefine this function, and call it in the init"
        )

    def binding_state(
        self,
        widget: QWidget,
        observable: ObservableProperty[bool] | ComputedObservableProperty[bool],
        prop: typing.Literal["visibility", "state", "readonly"],
    ) -> None:
        if prop == "visibility":
            observable.valueChanged += widget.setVisible
        if prop == "state":
            observable.valueChanged += widget.setEnabled
        if prop == "readonly" and hasattr(widget, "setReadOnly"):
            observable.valueChanged += widget.setReadOnly
        observable.valueChanged(observable.get())
        return None

    def binding_command(
        self,
        widget: typing.Union[
            QPushButton,
            QToolButton,
            QAction,
            QRadioButton,
        ],
        command: RelayCommand,
    ) -> None:
        if isinstance(widget, (QAction, QToolButton)):
            widget.triggered.connect(command)
        if isinstance(widget, QPushButton):
            widget.clicked.connect(command)
        if isinstance(widget, QRadioButton):
            widget.clicked.connect(command)
        return None

    def binding_rcommand(
        self,
        widget: QObject,
        command: RCommand,
    ) -> None:
        match widget:
            case QToolButton():
                widget.triggered.connect(command)
            case QPushButton():
                widget.clicked.connect(command)
            case QRadioButton():
                widget.clicked.connect(command)
            case QAction():
                widget.triggered.connect(command)
            case _:
                raise Exception(f"Cant bind this widget: {widget.__class__}")
        return None

    def binding_selection(
        self,
        widget: QComboBox,
        observable: ObservableCollection[T],
        *,
        observable_value: typing.Union[
            ObservableProperty[typing.Any],
            ComputedObservableProperty[typing.Any],
        ]
        | None = None,
        default_select: bool = False,
        visible_items: int = 5,
        converter: IValueConverter[typing.Any, str] | None = None,
    ) -> None:
        widget.setDuplicatesEnabled(False)
        widget.setMaxVisibleItems(visible_items)

        def _update_widget(
            values: typing.List[typing.Any],
        ) -> None:
            _current_text = widget.currentText()
            widget.clear()

            for value in values:
                if isinstance(value, (str, int, float)):
                    widget.addItem(str(value), userData=QVariant(value))
                elif not converter:
                    raise ValueError("Please provide a converter")
                else:
                    widget.addItem(converter.convert(value), userData=QVariant(value))
            widget.setCurrentText(_current_text)
            return None

        def _update_observable_value() -> None:
            observable_value.set(widget.currentData())
            return None

        observable.valueChanged += _update_widget
        observable.valueChanged(observable.collection)
        widget.setCurrentIndex(0) if default_select else widget.setCurrentIndex(-1)

        if observable_value is not None:
            widget.currentTextChanged.connect(_update_observable_value)
            widget.currentTextChanged.emit(widget.currentText())
        return None

    def binding_combobox_selection(
        self,
        widget: QComboBox,
        observable: typing.Union[
            ObservableProperty[typing.Any],
            ComputedObservableProperty[typing.Any],
        ],
    ) -> None:
        warnings.warn(
            "WARN: depracted feature, will be removed soon [use instead <binding_selection> method]"
        )
        widget.currentTextChanged.connect(lambda: observable.set(widget.currentData()))
        widget.currentTextChanged.emit(widget.currentText())
        # widget.currentTextChanged.emit(widget.currentData())
        # observable.set()
        return None

    def binding_combobox(
        self,
        widget: QComboBox,
        observable: ObservableCollection[typing.Any],
        selection_default: bool = False,
        display_name: typing.Optional[str] = None,
        visibles_items: int = 7,
    ) -> None:
        warnings.warn(
            "WARN: depracted feature, will be removed soon [use instead <binding_selection> method]"
        )
        widget.setDuplicatesEnabled(False)
        widget.setMaxVisibleItems(visibles_items)
        widget.clear()

        observable.valueChanged.connect(widget.clear)
        observable.valueChanged.connect(
            lambda values: self._fill_combobox_items(widget, values, display_name)
        )
        if selection_default:
            observable.valueChanged.emit(observable.collection)
            # widget.setCurrentIndex(0)
        else:
            observable.valueChanged.emit(observable.collection)
            widget.setCurrentIndex(-1)
        return None

    def binding_lineedit(
        self,
        widget: QLineEdit,
        observable: ObservableProperty[T] | ComputedObservableProperty[T],
        *,
        bindings: typing.Literal["on-typing", "on-typed"] = "on-typing",
        converter: IValueConverter[T, str] | None = None,
    ) -> None:
        def _update_widget(value: T):
            widget.setText(str(value))
            return None

        def _update_observable(value: typing.Any):
            _type: typing.Type = observable.__orig_class__.__args__[0]
            try:
                if _type in [int, float]:
                    value = _type(eval(widget.text()))
                elif _type in [str]:
                    value = _type(widget.text())
                else:
                    value = ""
                observable.set(value)
                return None

            except NameError:
                widget.clear()
            except SyntaxError:
                widget.clear()
            return None

        if bindings == "on-typing":
            widget.textChanged.connect(_update_observable)
        if bindings == "on-typed":
            widget.textChanged.connect(_update_observable)

        observable.valueChanged += _update_widget
        observable.valueChanged(observable.get())
        return None

    def binding_label(
        self,
        widget: QLabel,
        observable: typing.Union[ObservableProperty[T], ComputedObservableProperty[T]],
        converter: IValueConverter[T, typing.Any] | None = None,
    ) -> None:
        # _type: typing.Type = observable.__orig_class__.__args__[0]
        def _update_widget(value: T):
            if converter:
                widget.setText(converter.convert(value))
            else:
                widget.setText(str(value))

        observable.valueChanged += _update_widget
        _update_widget(observable.get())

        return None

    def binding_spinbox(
        self,
        widget: QSpinBox,
        observable: typing.Union[
            ObservableProperty[int],
            ComputedObservableProperty[int],
        ],
        converter: IValueConverter[int, int] | None = None,
    ) -> None:
        def _update_widget(value: int) -> None:
            widget.blockSignals(True)
            if converter:
                widget.setValue(converter.convert(value))
            else:
                widget.setValue(value)
            widget.blockSignals(False)

        def _update_observable(value: int) -> None:
            if converter:
                observable.set(converter.back_convert(value))
            else:
                observable.set(value)

        observable.valueChanged += _update_widget
        widget.valueChanged.connect(_update_observable)

        observable.valueChanged(observable.get())
        return None

    def binding_doublespinbox(
        self,
        widget: QDoubleSpinBox,
        observable: typing.Union[
            ObservableProperty[float],
            ComputedObservableProperty[float],
        ],
        converter: IValueConverter[typing.Any, typing.Any] | None = None,
    ) -> None:
        def _update_widget(value: float):
            widget.setValue
            return None

        def _update_observable(value: float):
            if converter:
                observable.set(converter.back_convert(value))
            else:
                observable.set(value)
            return None

        # if converter:
        #     observable.valueChanged += lambda value: widget.setValue(
        #         converter.convert(value)
        #     )
        #     widget.valueChanged.connect(
        #         lambda value: observable.set(converter.back_convert(value))
        #     )
        #     observable.valueChanged(observable.get())
        #     return None

        observable.valueChanged += _update_widget
        widget.valueChanged.connect(_update_observable)

        observable.valueChanged(observable.get())
        return None

    def binding_checkbox(
        self,
        widget: QCheckBox,
        observable: ObservableProperty[bool] | ComputedObservableProperty[bool],
    ) -> None:
        _type: typing.Type = observable.__orig_class__.__args__[0]
        if _type is not bool:
            raise ValueError("The observable must be a boolean type")

        def _update_widget(value: bool) -> None:
            widget.setChecked(value)
            return None

        def _update_observable(
            checked_state: int,
        ) -> None:
            match checked_state:
                case 2:
                    observable.set(True)
                case 0:
                    observable.set(False)
                case 1:
                    observable.set(False)
                case _:
                    return
            return None

        observable.valueChanged += _update_widget
        widget.stateChanged.connect(_update_observable)
        observable.valueChanged(observable.get())
        return None

    # Depracated function
    # Comboxbox
    def _binding_combobox_items(
        self,
        widget: QComboBox,
        observable: ObservableCollection[typing.Any],
        select_default: bool = True,
        max_visible_items: int = 7,
    ) -> None:
        # TODO: assume all value are converted into str before call addItems
        warnings.warn("WARN: Deprecated features (use binding_combobox insted)")
        widget.setDuplicatesEnabled(False)
        widget.setMaxVisibleItems(max_visible_items)
        observable.valueChanged += lambda v: widget.clear()
        observable.valueChanged += lambda values: self._fill_combobox_items(
            widget, values
        )
        if select_default:
            observable.valueChanged.emit(observable.collection)
            # widget.setCurrentIndex(0)
        else:
            widget.setCurrentIndex(-1)
            observable.valueChanged.emit(observable.collection)
        return None

    def _fill_combobox_items(
        self,
        widget: QComboBox,
        values: typing.List[typing.Any],
        display_name: typing.Optional[str] = None,
    ) -> None:
        for value in values:
            if isinstance(value, (str, int, float)):
                widget.addItem(str(value), userData=QVariant(value))
            else:
                if display_name:
                    _display_name = getattr(value, display_name, None)
                    if _display_name:
                        widget.addItem(_display_name, userData=QVariant(value))
                else:
                    widget.addItem(str(value), userData=QVariant(value))

        return None

    def _binding_combobox_value(
        self,
        widget: QComboBox,
        observable: typing.Union[
            ObservableProperty[str],
            ComputedObservableProperty[str],
        ],
    ) -> None:
        warnings.warn("WARN: deprecated function")
        # TODO: assume all value are converted into str before call addItems
        # widget.currentTextChanged.connect(observable.set) Old
        # widget.currentTextChanged.emit(widget.currentText)
        widget.currentTextChanged.connect(lambda: observable.set(widget.currentData()))
        widget.currentTextChanged.emit(widget.currentText())
        return None

    def binding_textedit(
        self, widget: QTextEdit, observable: ObservableProperty[str]
    ): ...
    def binding_datetimeedit(
        self, widget: QDateTimeEdit, observable: ObservableProperty[datetime]
    ):
        def _update_widget(value: date):
            widget.setDate(value)
            return None

        def _update_observable(value: QDateTime):
            observable.set(value.toPyDateTime())
            return None

        observable.valueChanged += _update_widget
        widget.dateTimeChanged.connect(_update_observable)
        observable.valueChanged(observable.get())
        return None

    def binding_dateedit(self, widget: QDateEdit, observable: ObservableProperty[date]):
        def _update_widget(value: date):
            widget.setDate(value)
            return None

        def _update_observable(value: QDate):
            observable.set(value.toPyDate())
            return None

        observable.valueChanged += _update_widget
        widget.dateChanged.connect(_update_observable)
        observable.valueChanged(observable.get())
        return None
