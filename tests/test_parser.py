"""Test of the various bits of the parser."""
# funsies
from fchic.parser_definition import (
    real_arr_deck,
    int_arr_deck,
    char_arr_deck,
    cval_deck,
    deck,
    details,
    fchk,
    header,
    integer,
    ival_deck,
    name_of_deck,
    real,
    rval_deck,
    title,
)


def test_data_types() -> None:
    """Test parsers for various types."""
    result = real.parseString("-6.20000000E+10")
    assert float("".join(result["base"])) == -6.2
    assert int(result["exponent"]) == 10
    assert int(integer.parseString("4")[0]) == 4
    assert int(integer.parseString("0")[0]) == 0
    assert int(integer.parseString("-0")[0]) == 0
    assert int(integer.parseString("+08")[0]) == 8
    assert int(integer.parseString("-118 +3")[0]) == -118


def test_header() -> None:
    """Test header parser."""
    ex_header = """TD-DFT calculation                                                      
Freq      RB3LYP                                                      6-31G(d)            
Number of atoms                            I               12
"""
    # test reading header
    assert "".join(title.parseString(ex_header)) == "TD-DFT calculation"
    result = details.parseString(ex_header.splitlines()[1])
    assert ["".join(word) for word in result] == ["Freq", "RB3LYP", "6-31G(d)"]
    result = header("header").parseString(ex_header)
    assert "title" in result["header"] and "details" in result["header"]


def test_deck_name() -> None:
    """Test deck name parser."""
    ex_block1 = "Current cartesian coordinates              R   N=          36\n"
    ex_block2 = "Number of independent functions            I              102\n"
    ex_block3 = """Info1-9                                    I   N=           9
            7           6           0           0           0         100
            6          18        -502"""
    assert (
        "".join(name_of_deck.parseString(ex_block1)) == "Current cartesian coordinates"
    )
    assert (
        "".join(name_of_deck.parseString(ex_block2))
        == "Number of independent functions"
    )
    assert "".join(name_of_deck.parseString(ex_block3)) == "Info1-9"


def test_decks() -> None:
    """Test reading of decks."""
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

    result = char_arr_deck.parseString("\n".join(example_decks.splitlines()[1:6]))
    assert "".join(result["key"]) == "Route"
    assert "".join(result["type"]) == "C"
    assert "".join(result["size"]) == "7"
    assert "".join(result["value"]) == "\n".join(example_decks.splitlines()[2:4])

    result = real_arr_deck.parseString("\n".join(example_decks.splitlines()[4:-1]))
    assert float(result.value[0]) == 6.0
    assert float(result.value[7]) == 1.0

    # Test reading all decks
    result = deck[...].parseString(example_decks)
    assert len(result) == 4


def test_full() -> None:
    """Test reading a fchk file."""
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
Virial Ratio                               R      2.010118722531438E+00
Atom Types                                 C   N=          12
                                                            
                                                            
                        
Int Atom Types                             I   N=          12
           0           0           0           0           0           0
           0           0           0           0           0           0
Nuclear charges                            R   N=          12
  6.00000000E+00  6.00000000E+00  6.00000000E+00  6.00000000E+00  6.00000000E+00
  6.00000000E+00  1.00000000E+00  1.00000000E+00  1.00000000E+00  1.00000000E+00
  1.00000000E+00  1.00000000E+00
"""
    data = fchk.parseString(ex_full)
    assert "header" in data
    assert "decks" in data
    print(data["decks"])
    assert len(data["decks"]) == 10
