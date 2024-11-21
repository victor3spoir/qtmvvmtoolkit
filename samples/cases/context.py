import sys
from pathlib import Path


def register_package():
    sys.path.insert(0, Path(__file__).parent.parent.parent.joinpath("src").as_posix())
    import qtmvvmtoolkit

    qtmvvmtoolkit.__file__
    return None


register_package()
