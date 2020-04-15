from jasminesnake import __version__

from antlr4 import *
from .lex import JavaScriptLexer, JavaScriptParser

import argparse
import colorama


arg_parser = argparse.ArgumentParser(
    description="Jasmine Snake, another JS interpreter in Python",
    epilog="I hope you don't use it, **especially** in production.",
)

arg_parser.add_argument("--snake", action="store_true", help="Print a snake")
args = arg_parser.parse_args()

JSL = JavaScriptLexer.JavaScriptLexer
JSP = JavaScriptParser.JavaScriptParser


class WriteTreeListener(ParseTreeListener):
    def visitTerminal(self, node: TerminalNode):
        print("Visit Terminal: " + str(node) + " - " + repr(node))


def main():
    colorama.init()

    print("Jasmine Snake v{version}".format(version=__version__))

    if args.snake:
        print(
            colorama.Style.DIM
            + "[snake is sleeping now, so you see this stub. pretend you see the snake, please.]"
        )
        print(
            colorama.Fore.BLACK
            + colorama.Back.YELLOW
            + "Don't tread on me!"
            + colorama.Back.RESET
            + colorama.Fore.RESET
        )

    print()

    input_stream = InputStream('"use strict";var a;\na=2+a;')
    lexer = JSL(input_stream)
    stream = CommonTokenStream(lexer)
    parser = JSP(stream)
    print("Created parsers")
    tree = parser.program()
    ParseTreeWalker.DEFAULT.walk(WriteTreeListener(), tree)


if __name__ == "__main__":
    main()
