# coding:utf-8


from typing import Any, Dict
from pydantic import BaseModel
from qtmvvmtoolkit.commands import rcommand
from qtmvvmtoolkit.inputs import observable_object, IObservableObject


@observable_object
class User(IObservableObject):
    def __init__(self, name: str = "vik", age: int = 9) -> None:
        self.name = name
        self.age = age
        return


@observable_object
class CUser(IObservableObject):
    name: str = "vik"
    age: int = 3


class UserInfo(BaseModel, IObservableObject):
    name: str = "vik"
    age: int = 25


@observable_object
class UserInfoState(BaseModel, IObservableObject):
    name: str = "viktor"
    age: int = 25

    def get_attribute(self) -> Dict[str, Any]:
        return UserInfo(**super().get_attribute())


class UserViewModel:
    def __init__(self):
        super().__init__()
        self.user = UserInfoState()
        # Messenger.Default.use(HelloMessage, self.command_handle_message)
        self.user.set_attribute(dict(age=33))
        return

    # @rcommand()
    def command_display_user(self) -> None:
        print(self.user.get_attribute())
        return None
