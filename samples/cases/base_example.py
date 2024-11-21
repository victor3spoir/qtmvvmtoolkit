# coding:utf-8
import sys
from PyQt6.QtWidgets import *
from qtmvvmtoolkit.objects import BindableObject


class SimpleDataBindingViewModel:
    def __init__(self) -> None:
        return


class SimpleDataBindingWidget(QWidget, BindableObject):
    def __init__(self, vm: SimpleDataBindingViewModel):
        super().__init__()
        self.vm = vm

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<h1>Simple Application</h1>"))
        pass


app = QApplication(sys.argv)
w = SimpleDataBindingWidget(SimpleDataBindingViewModel())
w.show()
app.exec()
