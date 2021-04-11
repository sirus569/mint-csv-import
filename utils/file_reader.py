import pathlib


def read_cookies() -> str:
    current_path = pathlib.Path(__file__).parent.absolute()
    absolute_path = pathlib.Path().joinpath(
        current_path,
        "..",
        ".locals",
        ".cookie"
    )
    _cookie = ""

    with open(absolute_path, "r") as inputFile:
        _cookie = inputFile.read()

    return _cookie