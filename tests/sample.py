from dataclasses import dataclass
import context
from qtmvvmtoolkit.inputs import ObservableClassV2

context.__file__


@dataclass
class UUser(ObservableClassV2):
    email: str = "viktor"
    age: int = 25


def main():
    u = UUser()
    # u.bind(lambda k, v: print(f"sameple {k}->{v}"))
    # u.name = "espoir"
    # u.age = 39
    # print("espoir - 39", u.bindable("name", str).get(), u.bindable("age", int).get())
    u.bindable("email", str).set("espoir(2)")
    # u.bindable("age", int).set(40)
    # print("bindable name", u.bindable("name", str).get(), u.name)
    # print("bindable age", u.bindable("age", str).get(), u.age)
    # b.set("new_user")
    # b.set("another user one")
    # print("sample result", u.to_dict(), u._bindables, sep="\n")
    print(u._bindables)
    return


if __name__ == "__main__":
    main()
