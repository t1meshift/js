# Jasmine Snake
Another JavaScript interpreter written on Python 3.

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![SemVer: 2.0.0](https://img.shields.io/badge/SemVer-2.0.0-F8DE7E?labelColor=23261D)](https://semver.org/spec/v2.0.0.html)

## Requirements

- ANTLR 4
- Colorama

To run tests:

- pylint
- Tox

You can get ANTLR [here](https://www.antlr.org/), other dependencies could be installed with pip:
```bash
pip install -r requirements.txt # Use requirements-dev.txt if you want to run tests
```

## Running

```bash
antlr4 -o jasminesnake/lex -package lex -Dlanguage=Python3 grammars/*.g4
python -m jasminesnake
```

## Credits

JavaScript grammar source: 
[https://github.com/antlr/grammars-v4/tree/master/javascript/javascript](https://github.com/antlr/grammars-v4/tree/master/javascript/javascript)

The snake:
[https://textart.io/art/lnl9xe1OsKIow7xPGeWDrAeF/snake](https://textart.io/art/lnl9xe1OsKIow7xPGeWDrAeF/snake)