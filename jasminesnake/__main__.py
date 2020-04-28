"""Pylint tells me this module should have a docstring.
So here it is.
"""
import sys
import argparse
import logging
import colorama
import coloredlogs

from jasminesnake import __version__, __snake__, LOG_LEVELS
from .js_stream import JSBaseStream, JSStringStream, JSFileStream
from .lex.ErrorListeners import LogErrorListener
from .ast import to_ascii_tree, from_parse_tree


def create_argument_parser():
    _arg_parser = argparse.ArgumentParser(
        description="Jasmine Snake, another JS interpreter in Python",
        epilog="I hope you don't use it, **especially** in production.",
    )

    _arg_parser.add_argument("--snake", action="store_true", help="print a snake")
    _arg_parser.add_argument(
        "--verbose",
        "-v",
        action="count",
        default=0,
        help="be more verbose. up to 4 (-vvvv) could be handled, more are ignored",
    )
    _arg_parser.add_argument(
        "infile",
        type=str,
        help='JS input file. use "-" to read input from stdin.',
        nargs="?",
    )

    return _arg_parser


def main():
    # Init colorama
    colorama.init()

    # Init logging
    log_level = min(args.verbose, 4)  # Ignore verbosity values more than 4
    coloredlogs.install(
        level=LOG_LEVELS[log_level]["level"], fmt=LOG_LEVELS[log_level]["format"]
    )

    # Print the snake if an argument is present
    if args.snake:
        print(colorama.Style.DIM + __snake__ + colorama.Style.RESET_ALL)
        print(
            colorama.Fore.BLACK
            + colorama.Back.YELLOW
            + "Don't tread on me!"
            + colorama.Back.RESET
            + colorama.Fore.RESET
        )

    # Read JS code from file or stdin
    if args.infile is not None:
        stream: JSBaseStream

        if args.infile == "-":
            input_str = sys.stdin.read()
            stream = JSStringStream(input_str)

        else:
            stream = JSFileStream(args.infile, LogErrorListener())

        tree = stream.parse()

        ast_tree = from_parse_tree(tree)
        ascii_ast = to_ascii_tree(ast_tree)

        logging.info("Got an AST!\n%s", ascii_ast)
        # TODO: run logic
        sys.exit(0)

    print("Jasmine Snake v{version}".format(version=__version__))
    print(
        colorama.Fore.YELLOW
        + "Notice that only single-line statements are supported."
        + colorama.Fore.RESET
    )
    print()

    try:
        while True:
            input_str = input("> ")
            logging.debug("Got input %s", input_str)

            stream = JSStringStream(input_str, LogErrorListener())
            tree = stream.parse()
            logging.debug("Got tree %s", tree.toStringTree(stream.parser.ruleNames))

            ast_tree = from_parse_tree(tree)
            ascii_ast = to_ascii_tree(ast_tree)

            logging.info("Got an AST!")
            logging.info(ascii_ast)
            # TODO: run logic
    except EOFError:
        print("Ctrl-D received, shutting down...")
        sys.exit(0)


if __name__ == "__main__":
    arg_parser = create_argument_parser()
    args = arg_parser.parse_args()
    main()
