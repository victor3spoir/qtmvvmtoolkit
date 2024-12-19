# import typing

# import context

# context.__file__

# from qtmvvmtoolkit.inputs import ObservableObjectDev


# class User:
#     def __init__(self) -> None:
#         self.username: str = "default"
#         self.age: int = 0
#         self.account: float = 0
#         return


# user = User()


# def func(arg: typing.Union[User, typing.Any]):
#     return


# func(user.account)


# o_user = ObservableObjectDev[User](user)
# o_user.binding_port(user.username).set("espoirt")
# o_user.binding_port("age").set(20)
# o_user.binding_port("account").set(2000)
# print(user.__dict__)
