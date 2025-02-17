# coding:utf-8
from qtmvvmtoolkit.commands import RelayCommand
from qtmvvmtoolkit.converters import IValueConverter
from qtmvvmtoolkit.objects import QtBindableObject
from qtpy.QtGui import *
from qtpy.QtWidgets import *
from viewmodels.homevm import HomeViewModel


class PercentageConverter(IValueConverter[float, float]):
    def convert(self, value: float) -> float:
        return value * 100

    def back_convert(self, value: float) -> float:
        return value / 100


class IntPercentageConverter(IValueConverter[int, int]):
    def convert(self, value: int) -> int:
        return int(value * 100)

    def back_convert(self, value: int) -> int:
        return int(value / 100)


class CaptitalizeConverter(IValueConverter[str, str]):
    def convert(self, value: str) -> str:
        return value.upper() + "_suffix"

    def back_convert(self, value: str) -> str:
        return value.lower()[-8:]


class PageHome(QWidget, QtBindableObject):
    def __init__(self) -> None:
        super().__init__()
        self.vm = HomeViewModel()

        self.initialize_component()
        self.initialize_binding()

        for number in self.vm.numbers:
            print(number)
        ...

    def initialize_component(self):
        lay = QHBoxLayout()
        lay.addStretch()

        layout = QVBoxLayout(self)
        layout.addLayout(lay)

        self.entryName = QLineEdit(self)
        self.labelName = QLabel("--#--", self)
        self.labelVoltage = QLabel("V")

        self.spinCapacity = QDoubleSpinBox()
        self.spinVoltage = QSpinBox()
        self.spinEnergy = QDoubleSpinBox()
        self.spinEnergy.setReadOnly(True)
        self.spinEnergy.setMaximum(9999999)
        self.spinVoltage.setMaximum(9999999)
        self.checkNumbers = QCheckBox(self)

        self.cboxNames = QComboBox(self)
        self.entry_cbox_value = QLineEdit()
        self.entry_for_number = QLineEdit()

        self.buttonCall = QPushButton("Caller")
        self.buttonNewCommand = QPushButton("Test New Command")
        # self.buttonCall.setProperty()

        layout.addWidget(QLabel("<h2>Observables Str Properties</h2>"))
        layout.addWidget(self.entryName)
        layout.addWidget(self.labelName)
        layout.addSpacing(10)
        layout.addWidget(QLabel("<h2>Computed Properties Sections</h2>"))
        layout.addWidget(QLabel("Voltage"))
        layout.addWidget(self.spinVoltage)
        layout.addWidget(self.labelVoltage)
        layout.addWidget(QLabel("Capacity"))
        layout.addWidget(self.spinCapacity)
        layout.addWidget(self.spinEnergy)

        layout.addWidget(QLabel("<h2>Relayables Properties Sections</h2>"))
        layout.addWidget(self.buttonCall)
        layout.addWidget(self.buttonNewCommand)
        layout.addWidget(QLabel("<h2>Observables Collections</h2>"))
        layout.addWidget(self.cboxNames)
        layout.addWidget(self.entry_cbox_value)
        layout.addWidget(self.entry_for_number)
        layout.addWidget(self.checkNumbers)
        layout.addStretch()

        return None

    def initialize_binding(self) -> None:
        self.binding_label(
            self.labelName, self.vm.username, converter=CaptitalizeConverter()
        )
        self.binding_spinbox(
            self.spinVoltage, self.vm.voltage, converter=IntPercentageConverter()
        )
        self.vm.voltage.binding(self.spinVoltage.setValue)

        self.binding_lineedit(self.entryName, self.vm.username)
        self.binding_checkbox(self.checkNumbers, self.vm.state)
        self.binding_spinbox(self.spinVoltage, self.vm.voltage)
        self.binding_label(
            self.labelVoltage, self.vm.voltage, string_format="Updated: {:5.10f}"
        )
        self.binding_state(self.spinVoltage, self.vm.hide, prop="visibility")
        self.binding_doublespinbox(self.spinCapacity, self.vm.capacity)
        self.binding_command(self.buttonCall, RelayCommand(self.display_information))
        self.binding_command(self.buttonNewCommand, self.vm.command_test_new_command)

        self.binding_selection(
            self.cboxNames,
            self.vm.user_infos,
            selection_default=False,
            display_name="infos",
            observable_value=self.vm.user,
        )
        self.binding_lineedit(self.entry_for_number, self.vm.counter)
        return None

    def display_information(self):
        self.launch_operation()
        self.vm.fill_numbers()
        return None

    def launch_operation(self):
        self.vm.hide.set(not self.vm.hide.get())
        print(self.vm.user.get())
        return None
