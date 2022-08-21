from typing import Any


def assertListOfObj(theList: list[Any] = None, theObject: Any = None) -> bool:
    return isinstance(theList, list) and all(isinstance(line, theObject) for line in theList)


def getIndex(phrase: str, lines: list[str], full: bool = False) -> int:
    assert isinstance(phrase, str)
    assertListOfObj(lines, str)
    assert isinstance(full, bool)

    if full:
        try:
            return lines.index(phrase)
        except ValueError:
            return -1

    else:
        for num, line in enumerate(lines):
            if phrase in line:
                return num

        return -1
