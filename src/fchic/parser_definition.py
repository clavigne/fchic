"""fchic is a generic parser for Gaussian formatted checkpoint files."""
# external
from pyparsing import (
    Combine,
    Group,
    LineEnd,
    LineStart,
    Literal,
    nums,
    oneOf,
    OneOrMore,
    ParserElement,
    printables,
    SkipTo,
    StringEnd,
    StringStart,
    White,
    Word,
)

ParserElement.enablePackrat()  # faster
ParserElement.setDefaultWhitespaceChars(" \t")  # use significant newlines


# Data types
# ------------------------------------------------------------------------------------------
# integer
integer = Word(nums + "+-")  # integer

# floating point
fp = Combine(Word(nums + "+-") + Literal(".") + Word(nums))

# fortran real
exp = oneOf("E e D d")
real = Combine(fp("base") + exp.setParseAction(lambda x: "e") + integer("exponent"))

# C type
char = Word(printables)

# Decks of data
# ------------------------------------------------------------------------------------------
# prelim
data_type = oneOf("R I C")
name_of_deck = LineStart() + OneOrMore(
    Word(printables), stopOn=White(min=3) + data_type
).setParseAction(" ".join)

# single value decks
ival_deck = name_of_deck("key") + Literal("I")("type") + integer("value")
rval_deck = name_of_deck("key") + Literal("R")("type") + real("value")
cval_deck = name_of_deck("key") + Literal("C")("type") + char("value")

# we have to parse this one differently
char_arr_deck = (
    name_of_deck("key")
    + Literal("C")("type")
    + Literal("N=").suppress()
    + integer("size")
    + LineEnd().suppress()
    + Group(SkipTo(LineEnd() + name_of_deck + data_type) | SkipTo(StringEnd()))("value")
)

real_arr_deck = (
    name_of_deck("key")
    + Literal("R")("type")
    + Literal("N=").suppress()
    + integer("size")
    + LineEnd().suppress()
    + Group(real.ignore("\n")[...])("value")
)

int_arr_deck = (
    name_of_deck("key")
    + Literal("I")("type")
    + Literal("N=").suppress()
    + integer("size")
    + LineEnd().suppress()
    + Group(integer.ignore("\n")[...])("value")
)
# fchck file header
# ------------------------------------------------------------------------------------------
title = (LineStart() + SkipTo(LineEnd())).setParseAction(lambda x: "".join(x).strip())
details = LineStart() + OneOrMore(Word(printables))
header = Group(
    title("title") + LineEnd().suppress() + details("details") + LineEnd().suppress()
)

# Formatted file definition
# ------------------------------------------------------------------------------------------
deck = (
    Group(
        char_arr_deck | real_arr_deck | int_arr_deck | ival_deck | rval_deck | cval_deck
    )
    + LineEnd().suppress()
)
fchk = (
    StringStart() + header("header") + deck[...]("decks")
)  # header + any number of decks
