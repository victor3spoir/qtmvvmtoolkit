# coding:utf-8
from qtmvvmtoolkit.commands import RelayCommand
from qtmvvmtoolkit.converters import ToStrConverter
from qtmvvmtoolkit.objects import BindableObject
from qtpy.QtGui import *
from qtpy.QtWidgets import *
from viewmodels.homevm import HomeViewModel


class PageHome(QWidget, BindableObject):
    def __init__(self) -> None:
        super().__init__()
        self.vm = HomeViewModel()

        self.initialize_component()
        self.initialize_binding()

        print("<===>")
        print(6 in self.vm.numbers)
        print(self.vm.numbers.pop(3))
        for number in self.vm.numbers:
            print(number)
        return

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
        layout.addWidget(self.spinVoltage)
        layout.addWidget(self.labelVoltage)
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
        self.binding_value(self.labelName, self.vm.username)
        # self.vm.username.binding(self.entryName.setText)
        # self.vm.username.binding(self.labelName.setText)
        # self.vm.username.rbinding(self.entryName.textChanged)
        # self.vm.username.binding(lambda v: print(f"==>{v}"))
        self.binding_value(self.spinVoltage, self.vm.voltage, use_percentage=True)
        self.vm.voltage.binding(self.spinVoltage.setValue)
        # self.vm.voltage.rbinding(self.spinVoltage.valueChanged)
        # self.vm.voltage.binding(lambda v: print(f"value===>{v}"))

        converter = ToStrConverter(str, str)
        converter.convert(8)
        self.binding_value(self.entryName, self.vm.username)
        self.binding_value(self.checkNumbers, self.vm.state)
        self.binding_value(self.spinVoltage, self.vm.voltage, use_percentage=True)
        self.binding_value(
            self.labelVoltage, self.vm.voltage, string_format="Updated: {:5.10f}"
        )
        self.binding_state(self.spinVoltage, self.vm.hide, prop="visibility")
        self.binding_value(self.spinCapacity, self.vm.capacity)
        # self.binding_value(self.spinEnergy, self.vm.energy)
        self.binding_command(self.buttonCall, RelayCommand(self.display_information))
        self.binding_command(self.buttonNewCommand, self.vm.command_test_new_command)

        self.binding_selection(
            self.cboxNames,
            self.vm.user_infos,
            selection_default=False,
            display_name="infos",
            observable_value=self.vm.user,
        )
        self.binding_value(self.entry_for_number, self.vm.counter)
        return None

    def display_information(self):
        self.launch_operation()
        self.vm.fill_numbers()
        return None

    def launch_operation(self):
        self.vm.hide.set(not self.vm.hide.get())
        print(self.vm.user.get())
        return None
