# coding:utf-8


import typing


TS = typing.TypeVar("TS")
TD = typing.TypeVar("TD")


class IValueConverter(typing.Generic[TS, TD]):
    def convert(self, value: TS) -> TD:
        raise NotImplementedError("Should be implemented")

    def back_convert(self, value: TD) -> TS:
        raise NotImplementedError("Should be implemented")


class IntToStrConveter(IValueConverter[int, str]):
    def convert(self, value: int) -> str:
        return str(value)

    def back_convert(self, value: str) -> int:
        return int(eval(value))
