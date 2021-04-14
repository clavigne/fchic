from pyparsing import (
    SkipTo,
    Literal,
    StringStart,
    Forward,
    Suppress,
    Group,
    Word,
    oneOf,
    White,
    StringEnd,
    LineStart,
    LineEnd,
    nums,
    Combine,
    printables,
    OneOrMore,
    printables,
    alphanums,
    ParserElement,
)


# newlines are significant
ParserElement.setDefaultWhitespaceChars(" \t")


# Data types
# ------------------------------------------------------------------------------------------
# integer
integer = Word(nums + "+-")  # integer

# floating point
fp = Word(nums + "-+.")  # fp

# fortran real
exp = oneOf("E e D d")
real = Combine(fp("base") + exp + integer("exponent"))

# C type
char = Word(printables)

# Decks of data
# ------------------------------------------------------------------------------------------
# prelim
data_type = oneOf("R I C")
name_of_deck = LineStart() + OneOrMore(
    Word(alphanums + "-" + "/"), stopOn=White(min=3) + data_type
).setParseAction(" ".join)

# single value decks
ival_deck = name_of_deck("key") + Literal("I")("type") + integer("value")
rval_deck = name_of_deck("key") + Literal("R")("type") + real("value")
cval_deck = name_of_deck("key") + Literal("C")("type") + char("value")

arr_deck = (
    name_of_deck("key")
    + data_type("type")
    + Literal("N=").suppress()
    + integer("size")
    + LineEnd().suppress()
    + Group(
        SkipTo(LineEnd() + name_of_deck + data_type).ignore("\n") | SkipTo(StringEnd())
    )("value")
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
deck = Group(arr_deck | ival_deck | rval_deck | cval_deck) + LineEnd().suppress()
fchk = (
    StringStart() + header("header") + deck[...]("decks")
)  # header + any number of decks

# Tests
# ------------------------------------------------------------------------------------------
# test data types
result = real.parseString("-6.20000000E+10")
assert float("".join(result["base"])) == -6.2
assert int(result["exponent"]) == 10
assert int(integer.parseString("4")[0]) == 4
assert int(integer.parseString("0")[0]) == 0
assert int(integer.parseString("-0")[0]) == 0
assert int(integer.parseString("+08")[0]) == 8
assert int(integer.parseString("-118 +3")[0]) == -118

ex_header = """TD-DFT calculation                                                      
Freq      RB3LYP                                                      6-31G(d)            
Number of atoms                            I               12
"""
# test reading header
assert "".join(title.parseString(ex_header)) == "TD-DFT calculation"
result = details.parseString(ex_header.splitlines()[1])
assert ["".join(word) for word in result] == ["Freq", "RB3LYP", "6-31G(d)"]
result = header("header").parseString(ex_header)

# test deck name parsers
ex_block1 = "Current cartesian coordinates              R   N=          36\n"
ex_block2 = "Number of independent functions            I              102\n"
ex_block3 = """Info1-9                                    I   N=           9
           7           6           0           0           0         100
           6          18        -502"""
assert "".join(name_of_deck.parseString(ex_block1)) == "Current cartesian coordinates"
assert "".join(name_of_deck.parseString(ex_block2)) == "Number of independent functions"
assert "".join(name_of_deck.parseString(ex_block3)) == "Info1-9"

# Test reading various deck types
example_decks = """Number of alpha electrons                  I               21
Route                                      C   N=           7
# Geom=AllCheck Guess=Read SCRF=Check GenChk B3LYP/6-31G(d) 
Symm=None Freq=(NoRaman)
Nuclear charges                            R   N=          12
  6.00000000E+00  6.00000000E+00  6.00000000E+00  6.00000000E+00  6.00000000E+00
  6.00000000E+00  1.00000000E+00  1.00000000E+00  1.00000000E+00  1.00000000E+00
  1.00000000E+00  1.00000000E+00
Virial Ratio                               R      2.010118722531438E+00
"""
result = ival_deck.parseString(example_decks.splitlines()[0])
assert "".join(result["key"]) == "Number of alpha electrons"
assert "".join(result["type"]) == "I"
assert "".join(result["value"]) == "21"

result = rval_deck.parseString(example_decks.splitlines()[-1])
assert "".join(result["key"]) == "Virial Ratio"
assert "".join(result["type"]) == "R"
assert "".join(result["value"]["base"]) == "2.010118722531438"
assert "".join(result["value"]["exponent"]) == "+00"

result = arr_deck.parseString("\n".join(example_decks.splitlines()[1:6]))
assert "".join(result["key"]) == "Route"
assert "".join(result["type"]) == "C"
assert "".join(result["size"]) == "7"
assert "".join(result["value"]) == "\n".join(example_decks.splitlines()[2:4])

result = arr_deck.parseString("\n".join(example_decks.splitlines()[4:-1]))
assert "".join(result["value"]) == "\n".join(example_decks.splitlines()[5:-1]).lstrip()

# Test reading all decks
result = deck[...].parseString(example_decks)
assert len(result) == 4


# Test header and blocks
ex_full = """TD-DFT calculation                                                      
Freq      RB3LYP                                                      6-31G(d)            
Number of atoms                            I               12
Info1-9                                    I   N=           9
           7           6           0           0           0         100
           6          18        -502
Multiplicity                               I                1
Number of electrons                        I               42
Number of alpha electrons                  I               21
Route                                      C   N=           7
# Geom=AllCheck Guess=Read SCRF=Check GenChk B3LYP/6-31G(d) 
Symm=None Freq=(NoRaman)
Nuclear charges                            R   N=          12
  6.00000000E+00  6.00000000E+00  6.00000000E+00  6.00000000E+00  6.00000000E+00
  6.00000000E+00  1.00000000E+00  1.00000000E+00  1.00000000E+00  1.00000000E+00
  1.00000000E+00  1.00000000E+00
"""

with open("test_data/gaussian_hessian/s0.fchk", "r") as f:
    full = f.read()

print(fchk.parseString(ex_full))

full = fchk.parseString(full)
print(full["decks"])
