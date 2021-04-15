"""fchic is a generic parser for Gaussian formatted checkpoint files."""
# std
from typing import Dict, List, TextIO, Union

# external
from pyparsing import ParseResults

# module
from .parser_definition import deck, fchk

Deck = Union[List[str], List[int], List[float]]
"""Type of a single deck from a fchk file."""

FchkOut = Dict[str, Deck]
"""Type of the output from parsing a full fchk file.."""


def _to_deck(group: ParseResults) -> Deck:
    """Parse a deck into a python list."""
    result: Deck
    if "size" in group:
        N = int(group["size"])
        if group["type"] == "C":
            result = ["".join(group.value)]
        elif group["type"] == "I":
            result = [int("".join(k)) for k in group.value]
            if len(result) != N:
                raise RuntimeWarning(f"expected {N} integers, got {len(result)}")
        elif group["type"] == "R":
            result = [float("".join(k)) for k in group.value]
            if len(result) != N:
                raise RuntimeWarning(f"expected {N} reals, got {len(result)}")
        else:
            raise TypeError(f'{group["type"]} is not one of C, I or R')
    else:
        if group["type"] == "C":
            result = ["".join(group.value)]
        elif group["type"] == "I":
            result = [int("".join(group.value))]
        elif group["type"] == "R":
            result = [float("".join(group.value))]
        else:
            raise TypeError(f'{group["type"]} is not one of C, I or R')

    return result


def _to_dict(inp: ParseResults) -> FchkOut:
    """Parse a formatted check point into a dictionary."""
    result: FchkOut = {}
    result["header"] = [
        "".join(inp["header"]["title"]),
        " ".join(inp["header"]["details"]),
    ]

    decks = inp.decks
    for group in decks:
        key = "".join(group["key"])
        result[key] = _to_deck(group)

    return result


def loads(inp: str) -> FchkOut:
    """Parse formatted checkpoint file from a string."""
    return _to_dict(fchk.parseString(inp))


def load(inp: TextIO) -> FchkOut:
    """Parse formatted checkpoint file from a filelike object."""
    return _to_dict(fchk.parseString(inp.read()))


def deck_loads(inp: str, name: str) -> Deck:
    """Parse single deck from a formatted checkpoint in string."""
    where = inp.find(name)

    if where < 0:
        raise AttributeError(f"{name} could not be found in input string.")

    group = deck.parseString(inp[where:])[0]
    my_name = "".join(group["key"])
    if my_name.strip() != name.strip():
        raise RuntimeWarning(f"expected deck {name}, but got a deck named {my_name}")
    return _to_deck(group)


def deck_load(inp: TextIO, name: str) -> Deck:
    """Parse single deck from a formatted checkpoint in a filelike object."""
    start_pos = inp.tell()
    for line in inp:
        if name in line:
            break
    else:
        inp.seek(start_pos)  # return to start pos
        raise AttributeError(f"{name} could not be found in input string.")

    rest = line + "\n" + inp.read()  # read rest of file
    inp.seek(start_pos)  # return to start_pos

    # parse rest
    group = deck.parseString(rest)[0]
    my_name = "".join(group["key"])
    if my_name.strip() != name.strip():
        raise RuntimeWarning(f"expected deck {name}, but got a deck named {my_name}")
    return _to_deck(group)


# Version information
# We grab it from setup.py so that we don't have to bump versions in multiple
# places.
try:
    # std
    from importlib import metadata

    __version__ = metadata.version("fchic")
except ImportError:
    # Running on pre-3.8 Python; use importlib-metadata package
    # external
    import importlib_metadata

    __version__ = importlib_metadata.version("fchic")
