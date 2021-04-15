# fchic

fchic is a tiny library for parsing [Gaussian formatted
checkpoint files](https://gaussian.com/formchk/) into python data structures.
To use it, simply point it at a file and give it a deck to load, like so:

```python
import fchic

with open("data.fchk", "r") as f:
    out = fchic.deck_load(f, "Cartesian Gradient")
```

`out` is now a list of `3 x N` floating point numbers parsed from the
`Cartesian Gradient` section of `data.fchk`.

**Note:** fchic does no data validation (beyond shape and type), no physical
unit conversions and no integration into fancy data structures. It is entirely
a single page, simple [pyparsing](https://github.com/pyparsing/pyparsing/)
grammar. You'll need to do your own data processing from its outputs.


## Usage

fchic consists of four functions:

  * `fchic.load(fp)` transform a formatted checkpoint file in from a file-like
    object `fp` into a python dictionary of decks.
  * `fchic.deck_load(fp, name)` loads the specific deck `name` from file-like
    object `fp`.

Versions of those functions that acts on strings (`fchic.loads()` and
`fchic.deck_loads`) are also provided.

Decks are returned thinly parsed from the formatted checkpoint files:
  * Integer values (type `I`) are parsed into lists of python `int`.
  * Real values (type `R`) are parsed into lists of python `float`.
  * Char values (type `C`) are parsed into a unary list containing a string.

Python is not exactly fast, and neither is pyparsing, so you'll generally want
to use `fchic.deck_load()` which does not have to parse the whole file, and is
therefore way way 🐇 faster 🐇.

## Installation

```bash
pip install fchic
```

## License

fchic is provided under the MIT license.


  
