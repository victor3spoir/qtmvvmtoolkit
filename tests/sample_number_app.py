# coding:utf-8

# coding:utf-8
import sys

import context

context.__file__
from qtmvvmtoolkit.converters import IValueConverter

# coding:utf-8
from qtmvvmtoolkit.inputs import (
    ComputedObservableProperty,
    ObservableProperty,
)
from qtmvvmtoolkit.objects import BindableObject
from qtpy.QtWidgets import (
    QLabel,
    QSpinBox,
    QDoubleSpinBox,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QApplication,
)


class FloatToFloatConverter(IValueConverter[float, float]):
    def convert(self, value: float) -> float:
        return value

    def back_convert(self, value: float) -> float:
        return value


class IntToIntConverter(IValueConverter[int, int]):
    def convert(self, value: int) -> int:
        return int(value)

    def back_convert(self, value: int) -> int:
        return int(value)


class CaptitalizeConverter(IValueConverter[str, str]):
    def convert(self, value: str) -> str:
        return value.upper() + "_suffix"

    def back_convert(self, value: str) -> str:
        return value.lower()[-8:]


class FloatToStrConverter(IValueConverter[float, str]):
    def convert(self, value: float) -> str:
        return "{:.1f} Wh".format(value)

    def back_convert(self, value: str) -> float:
        return float(eval(value))


class HomeViewModel:
    def __init__(self):
        super().__init__()

        self.voltage = ObservableProperty[int](48)
        self.capacity = ObservableProperty[int](100)
        self.energy = ComputedObservableProperty[float](
            self.compute_energy(), [self.voltage, self.capacity], self.compute_energy
        )
        ...

    def compute_energy(self) -> float:
        return self.voltage.get() * self.capacity.get()


class HomePage(QWidget, BindableObject):
    def __init__(self, vm: HomeViewModel) -> None:
        super().__init__()
        self.vm = vm

        self.initialize_component()
        self.initialize_binding()

    def initialize_component(self):
        lay = QHBoxLayout()
        lay.addStretch()

        layout = QVBoxLayout(self)
        layout.addLayout(lay)

        self.labelVoltage = QLabel("Voltage:")
        self.labelCapacity = QLabel("Capacity:")
        self.labelEnergy = QLabel("Energy:")
        self.spinCapacity = QSpinBox()
        self.spinVoltage = QSpinBox()
        self.dSpinEnergy = QDoubleSpinBox()
        self.dSpinEnergy.setReadOnly(True)
        self.dSpinEnergy.setMaximum(9999999)
        self.spinVoltage.setMaximum(9999999)

        layout.addWidget(QLabel("<h2>Computed Properties Sections</h2>"))
        layout.addWidget(QLabel("Voltage"))
        layout.addWidget(self.spinVoltage)
        layout.addWidget(self.labelVoltage)
        layout.addWidget(QLabel("Capacity"))
        layout.addWidget(self.spinCapacity)
        layout.addWidget(self.labelCapacity)
        layout.addWidget(QLabel("Computed Energy"))
        layout.addWidget(self.dSpinEnergy)
        layout.addWidget(self.labelEnergy)

        return None

    def initialize_binding(self) -> None:
        self.binding_label(self.labelVoltage, self.vm.voltage)
        self.binding_label(self.labelCapacity, self.vm.capacity)
        self.binding_label(
            self.labelEnergy, self.vm.energy, converter=FloatToStrConverter()
        )
        self.binding_spinbox(
            self.spinVoltage, self.vm.voltage, converter=IntToIntConverter()
        )
        self.binding_spinbox(
            self.spinCapacity, self.vm.capacity, converter=IntToIntConverter()
        )
        self.binding_doublespinbox(
            self.dSpinEnergy, self.vm.energy, converter=FloatToFloatConverter()
        )

        return None


if __name__ == "__main__":
    from qdarktheme import load_palette, load_stylesheet

    app = QApplication([])
    app.setStyleSheet(load_stylesheet("auto"))
    app.setPalette(load_palette("auto"))
    home = HomePage(HomeViewModel())
    home.show()
    sys.exit(app.exec())
