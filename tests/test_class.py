"""Test of the various bits of the parser."""
# funsies
import fchic


def test_read_string() -> None:
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
Nuclear charges                            R   N=          12
  6.00000000E+00  6.00000000E+00  6.00000000E+00  6.00000000E+00  6.00000000E+00
  6.00000000E+00  1.00000000E+00  1.00000000E+00  1.00000000E+00  1.00000000E+00
  1.00000000E+00  1.00000000E+00
"""
    result = fchic.loads(ex_full)


def test_read_file() -> None:
    """Test reading a fchk file."""
    with open("tests/data/data-trunc.fchk", "r") as f:
        result = fchic.load(f)
    assert len(result["Alpha Orbital Energies"]) == 102
