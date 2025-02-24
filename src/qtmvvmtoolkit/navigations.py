# coding:utf-8
import typing

from qtpy.QtGui import QIcon
from qtpy.QtWidgets import (
    QPushButton,
    QStackedWidget,
    QTabWidget,
    QToolButton,
    QWidget,
)


class Navigator:
    def __init__(self) -> None:
        self._outlet: typing.Union[QTabWidget, QStackedWidget]
        self._routes: typing.Dict[str, QWidget] = {}
        ...

    @classmethod
    def current(cls):
        try:
            return Navigator.__Default
        except AttributeError:
            Navigator.__Default = Navigator()
            return Navigator.__Default

    def add_outlet(
        self,
        outlet: typing.Union[QStackedWidget, QTabWidget],
    ):
        self._outlet = outlet
        return None

    def add_route(self, route: str, widget: QWidget) -> None:
        if isinstance(widget, (QTabWidget)):
            self.__register_for_tab(route, widget)
        if isinstance(widget, (QStackedWidget)):
            self.__register_for_stacked(widget)
        self._routes.update({route: widget})
        return None

    def __register_for_tab(self, route: str, widget: QWidget) -> None:
        self._outlet.addTab(widget, route)
        return None

    def __register_for_stacked(self, widget: QWidget) -> None:
        self._outlet.addWidget(widget)
        return None

    def goto(self, route: str) -> None:
        _widget = self._routes.get(route)
        if _widget:
            self._outlet.setCurrentWidget(_widget)
        return None

    def bind_navigation(
        self,
        button: typing.Union[QPushButton, QToolButton],
        route: str,
        icon: typing.Optional[QIcon] = None,
    ) -> None:
        if icon:
            button.setIcon(icon)
        button.clicked.connect(lambda: self.goto(route))
        return None
