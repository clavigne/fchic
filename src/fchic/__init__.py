"""fchic is a generic parser for Gaussian formatted checkpoint files."""
# std
from os import PathLike
from typing import TextIO, Union, Dict, List


# module
from .parser_definition import fchk


def _to_dict(inp: "result") -> Dict[str, Union[List[str], List[int], List[float]]]:
    result = {}
    result["header"] = [
        "".join(inp["header"]["title"]),
        " ".join(inp["header"]["details"]),
    ]

    decks = inp.decks
    for group in decks:
        key = "".join(group["key"])
        if "size" in group:
            N = int(group["size"])
            if group["type"] == "C":
                result[key] = ["".join(group.value)]
            elif group["type"] == "I":
                result[key] = [int("".join(k)) for k in group.value]
                if len(result[key]) != N:
                    raise RuntimeWarning(
                        f"expected {N} integers, got {len(result[key])}"
                    )
            elif group["type"] == "R":
                result[key] = [float("".join(k)) for k in group.value]
                if len(result[key]) != N:
                    raise RuntimeWarning(f"expected {N} reals, got {len(result[key])}")
            else:
                raise TypeError(f'{group["type"]} is not one of C, I or R')
        else:
            if group["type"] == "C":
                result[key] = ["".join(group.value)]
            elif group["type"] == "I":
                result[key] = [int("".join(group.value))]
            elif group["type"] == "R":
                result[key] = [float("".join(group.value))]
            else:
                raise TypeError(f'{group["type"]} is not one of C, I or R')

    return result


def loads(inp: str):
    return _to_dict(fchk.parseString(inp))


def load(inp: TextIO):
    return _to_dict(fchk.parseString(inp.read()))
