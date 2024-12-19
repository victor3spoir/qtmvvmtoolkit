# coding:utf-8

import typing
import warnings

from qtpy.QtCore import QObject, Qt, QVariant
from qtpy.QtGui import QAction
from qtpy.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QSpinBox,
    QToolButton,
    QWidget,
    QTextEdit,
    QDateTimeEdit,
    QDateEdit,
)

from qtmvvmtoolkit.commands import RCommand, RelayCommand
from qtmvvmtoolkit.inputs import (
    ComputedObservableProperty,
    ObservableCollection,
    ObservableProperty,
)

T = typing.TypeVar("T")


class BindableObject(QObject):
    def __init__(
        self,
        parent: typing.Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        return

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
        observable: typing.Union[
            ObservableProperty[bool], ComputedObservableProperty[bool]
        ],
        prop: typing.Literal["visibility", "state", "readonly"],
    ) -> None:
        if prop == "visibility":
            observable.valueChanged += lambda v: widget.setVisible(bool(v))
        if prop == "state":
            observable.valueChanged += lambda v: widget.setEnabled(bool(v))
        if prop == "readonly":
            if hasattr(widget, "setReadOnly"):
                observable.valueChanged.connect(widget.setReadOnly)
        observable.valueChanged(observable.get())
        return None

    def binding_value(
        self,
        widget: QWidget,
        observable: typing.Union[ObservableProperty[T], ComputedObservableProperty[T]],
        *,
        string_format: typing.Optional[str] = None,
        mode: typing.Literal["1-way", "2-way"] = "2-way",
        bindings: typing.Literal["on-typing", "on-typed"] = "on-typed",
        use_percentage: bool | None = None,
    ) -> None:
        # use percentage is only reserved for qspinbox & qdoublespinbox
        # NOTE: this is about to know the type of observable
        # _type: type = typing.get_args(observable.__orig_class__)[0]

        match widget:
            case QLineEdit():
                self._binding_lineedit(widget, observable, bindings=bindings)
            case QLabel():
                self._binding_label(widget, observable, string_format)
            case QSpinBox():
                self._binding_spinbox(widget, observable, use_percentage)
            case QDoubleSpinBox():
                self._binding_doublespinbox(widget, observable, use_percentage)
            case QCheckBox():
                self._binding_checkbox(widget, observable)
            case QTextEdit():
                print("Not available")
            case QDateEdit():
                print("Not available")
            case QDateTimeEdit():
                print("Not available")
            case _:
                raise Exception("unhandled case.")
        return None

    # def binding_relayable(
    #     self,
    #     func: typing.Callable[[], None],
    #     relayable: RelayableProperty,
    # ) -> None:
    #     relayable.relayed.connect(func)
    #     return None

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
        selection_default: bool = False,
        display_name: typing.Optional[str] = None,
        visibles_items: int = 7,
    ) -> None:
        widget.setDuplicatesEnabled(False)
        widget.setMaxVisibleItems(visibles_items)
        widget.clear()

        observable.valueChanged += lambda v: widget.clear()
        observable.valueChanged += lambda values: self._fill_combobox_items(
            widget, values, display_name
        )
        if selection_default:
            observable.valueChanged(observable.collection)
            # widget.setCurrentIndex(0)
        else:
            observable.valueChanged(observable.collection)
            widget.setCurrentIndex(-1)

        if observable_value:
            widget.currentTextChanged.connect(
                lambda: observable_value.set(widget.currentData())
            )
            widget.currentTextChanged.emit(widget.currentText())
        return

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

    # Input widgets
    def _binding_lineedit(
        self,
        widget: QLineEdit,
        observable: typing.Union[ObservableProperty[T], ComputedObservableProperty[T]],
        *,
        string_format: str | None = None,
        bindings: typing.Literal["on-typing", "on-typed"] = "on-typing",
        disable_editing: bool = False,
    ) -> None:
        _type: typing.Type = observable.__orig_class__.__args__[0]

        def __handle_textedit_binding(
            widget: QLineEdit,
            observable: ObservableProperty[typing.Any],
        ) -> None:
            _type: typing.Type = observable.__orig_class__.__args__[0]
            try:
                _value: typing.Any
                if _type in [int, float]:
                    _value = _type(eval(widget.text()))
                elif _type in [str]:
                    _value = _type(widget.text())
                else:
                    _value = ""
                observable.set(_value)

            except NameError:
                widget.clear()
            except SyntaxError:
                widget.clear()
            return None

        if disable_editing:
            widget.setReadOnly(disable_editing)

        if bindings == "on-typing":
            widget.textChanged.connect(
                lambda: __handle_textedit_binding(widget, observable)
            )
            ...
        if bindings == "on-typed":
            widget.editingFinished.connect(
                lambda: __handle_textedit_binding(widget, observable)
            )

        if string_format:
            widget.setReadOnly(True)
            observable.valueChanged += lambda value: widget.setText(
                string_format.format(value)
            )
            observable.valueChanged(observable.get())
            return

        observable.valueChanged += lambda value: widget.setText(str(value))
        observable.valueChanged(observable.get())
        return None

    def _binding_label(
        self,
        widget: QLabel,
        observable: typing.Union[ObservableProperty[T], ComputedObservableProperty[T]],
        string_format: str | None = None,
    ) -> None:
        # _type: typing.Type = observable.__orig_class__.__args__[0]

        if string_format:
            observable.valueChanged += lambda value: widget.setText(
                string_format.format(value)
            )
            observable.valueChanged(observable.get())
            return
        observable.valueChanged += lambda value: widget.setText(str(value))
        observable.valueChanged(observable.get())

        return None

    # SpinBox
    def _binding_spinbox(
        self,
        widget: QSpinBox,
        observable: typing.Union[
            ObservableProperty[int],
            ComputedObservableProperty[int],
        ],
        # transformer: typing.Optional[typing.Literal["percent"]] = None,
        use_percentage: bool | None = None,
    ) -> None:
        if use_percentage:
            observable.valueChanged += lambda value: widget.setValue(int(value * 100))
            widget.valueChanged.connect(lambda value: observable.set(int(value / 100)))
            observable.valueChanged(observable.get())
            return None

        observable.valueChanged += lambda v: widget.setValue(v)
        widget.valueChanged.connect(observable.set)
        observable.valueChanged(observable.get())
        return None

    def _binding_doublespinbox(
        self,
        widget: QDoubleSpinBox,
        observable: typing.Union[
            ObservableProperty[float],
            ComputedObservableProperty[float],
        ],
        # transformer: typing.Optional[typing.Literal["percent"]] = None,
        use_percentage: bool | None = None,
    ) -> None:
        if use_percentage:
            observable.valueChanged += lambda value: widget.setValue(value * 100)
            widget.valueChanged.connect(lambda value: observable.set(value / 100))
            observable.valueChanged(observable.get())
            return None

        observable.valueChanged += lambda v: widget.setValue(v)
        widget.valueChanged.connect(lambda v: observable.set(v))
        observable.valueChanged(observable.get())
        return None

    # QCheckBox
    def _binding_checkbox(
        self,
        widget: QCheckBox,
        observable: typing.Union[
            ObservableProperty[bool],
            ComputedObservableProperty[bool],
        ],
    ) -> None:
        # TODO: handle each case along the checked state
        def __handle_checkbox_binding(
            widget: QCheckBox,
            observable: typing.Union[
                ObservableProperty[bool],
                ComputedObservableProperty[bool],
            ],
        ) -> None:
            if widget.checkState() == Qt.CheckState.Checked:
                observable.set(True)
            if widget.checkState() == Qt.CheckState.Unchecked:
                observable.set(False)
            return None

        observable.valueChanged += lambda v: widget.setChecked(bool(v))
        widget.stateChanged.connect(
            lambda: __handle_checkbox_binding(widget, observable)
        )
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

            # if isinstance(value, Path):
            #     widget.addItem(value.name, userData=QVariant(value))
            # else:
            #     widget.addItem(str(value), userData=QVariant(value))
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

    # def __handle_textedit_binding(
    #     self,
    #     widget: QLineEdit,
    #     observable: ObservableProperty[typing.Any],
    # ) -> None:
    #     print("called")
    #     _type: typing.Type = observable.__orig_class__.__args__[0]
    #     try:
    #         _value = _type(eval(widget.text()))
    #         observable.set(_value)
    #     except NameError:
    #         widget.clear()
    #     except SyntaxError:
    #         widget.clear()
    #     return None

    # def binding_textedit_number(
    #     self,
    #     widget: QLineEdit,
    #     observable: typing.Union[
    #         ObservableProperty[int],
    #         ObservableProperty[float],
    #         ComputedObservableProperty[int],
    #         ComputedObservableProperty[float],
    #     ],
    # ) -> None:
    #     warnings.warn("WARN: deprecated function")
    #     widget.setReadOnly(True)
    #     observable.valueChanged.connect(lambda value: widget.setText(str(value)))
    #     observable.valueChanged.emit(observable.get())
    #     return None

    # def binding_textedit_str(
    #     self,
    #     widget: QLineEdit,
    #     observable: typing.Union[
    #         ObservableProperty[str],
    #         ComputedObservableProperty[str],
    #     ],
    # ) -> None:
    #     warnings.warn("WARN: deprecated function")
    #     observable.valueChanged.connect(widget.setText)
    #     widget.textChanged.connect(observable.set)
    #     observable.valueChanged.emit(observable.get())
    #     return None

    # def binding_label_number(
    #     self,
    #     widget: QLabel,
    #     observable: ObservableProperty[typing.Any],
    #     #     ObservableProperty[float],
    #     #     ComputedObservableProperty[int],
    #     #     ComputedObservableProperty[float],
    #     # ],
    #     # transformer: typing.Optional[
    #     #     typing.Callable[[typing.Union[int, float]], str]
    #     # ] = None,
    #     string_format: str | None = None,
    # ) -> None:
    #     if not string_format:
    #         observable.valueChanged.connect(
    #             lambda value: widget.setText(str(value)),
    #         )
    #     # if transformer:
    #     #     observable.valueChanged.connect(
    #     #         lambda value: widget.setText(transformer((value))),
    #     #     )
    #     if string_format:
    #         observable.valueChanged.connect(
    #             lambda value: widget.setText(string_format.format(value)),
    #         )

    #     observable.valueChanged.emit(observable.get())
    #     return

    # def binding_label_string(
    #     self,
    #     widget: QLabel,
    #     observable: typing.Union[
    #         ObservableProperty[str], ComputedObservableProperty[str]
    #     ],
    # ) -> None:
    #     observable.valueChanged.connect(widget.setText)
    #     observable.valueChanged.emit(observable.get())
    #     return None

    # def __handle_checkbox_binding(
    #     self,
    #     widget: QCheckBox,
    #     observable: typing.Union[
    #         ObservableProperty[bool],
    #         ComputedObservableProperty[bool],
    #     ],
    # ) -> None:
    #     if widget.checkState() == Qt.CheckState.Checked:
    #         observable.set(True)
    #     if widget.checkState() == Qt.CheckState.Unchecked:
    #         observable.set(False)
    #     return None

    # Widgets
    # def binding_widget(
    #     self,
    #     widget: QWidget,
    #     observable: typing.Union[
    #         ObservableProperty[bool], ComputedObservableProperty[bool]
    #     ],
    #     prop: typing.Literal["visibility", "state", "readonly"],
    # ):
    #     if prop == "visibility":
    #         observable.valueChanged.connect(widget.setVisible)
    #     if prop == "state":
    #         observable.valueChanged.connect(widget.setEnabled)
    #     if prop == "readonly":
    #         if hasattr(widget, "setReadOnly"):
    #             observable.valueChanged.connect(widget.setReadOnly)
    #     observable.valueChanged.emit(observable.get())
    #     return None
