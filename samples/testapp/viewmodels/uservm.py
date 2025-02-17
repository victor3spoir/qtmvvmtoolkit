# coding:utf-8


import dataclasses
from qtmvvmtoolkit.inputs import ObservableClass


@dataclasses.dataclass
class ObsUser(ObservableClass):
    name: str = "viktor espoir"
    age: int = 26


class UserViewModel:
    def __init__(self):
        super().__init__()
        self.user = ObsUser()
        # Messenger.Default.use(HelloMessage, self.command_handle_message)
        return

    # @rcommand()
    def command_display_user(self) -> None:
        print(self.user.to_dict())
        return None
