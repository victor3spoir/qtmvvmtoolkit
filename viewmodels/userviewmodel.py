from mvvmkit.observables.observableproperty import ObservableProperty
from mvvmkit.observables._ObservableObject import ObservableObject
from mvvmkit.commands.relaycommand import RelayCommand


class UserViewModel(ObservableObject):
    def __init__(self) -> None:
        super().__init__()
        self.page_title = "UserPage"
        self.username = ObservableProperty("")
        self.email = ObservableProperty("")
        pass

    # @RelayCommand
    def command_send_info(self):
        _data = dict(username=self.username.get(),
                     email=self.email.get())
        print(_data)
        return _data
    pass
