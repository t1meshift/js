"""A module for JavaScript code stream creation and its parsing. """
from antlr4 import InputStream, CommonTokenStream, FileStream, StdinStream
from antlr4.error.ErrorListener import ErrorListener

from .lex import JavaScriptLexer, JavaScriptParser

JSL = JavaScriptLexer.JavaScriptLexer
JSP = JavaScriptParser.JavaScriptParser


class JSBaseStream:
    """JavaScript stream base class.

    Notes:
        Do not instantiate the base class.

    See Also:
         JSFileStream
         JSStringStream
         JSStdinStream
    """

    _input_stream: InputStream = None
    _error_listener = None
    lexer = None
    parser = None

    def __init__(self, error_listener):
        if self is JSBaseStream:
            raise TypeError(
                "JSReader is a base class, you should instantiate its subclasses instead."
            )

        self._error_listener = error_listener

    def parse(self) -> JSP.ProgramContext:
        """Parse the stream.

        Returns:
            Program context.
        """
        self.lexer = JSL(self._input_stream)
        stream = CommonTokenStream(self.lexer)
        self.parser = JSP(stream)

        # Register error listener if present
        if self._error_listener is not None:
            self.parser.removeErrorListeners()
            self.parser.addErrorListener(self._error_listener)

        return self.parser.program()


class JSStringStream(JSBaseStream):
    """JavaScript string stream.

    See Also:
        JSBaseStream
        JSFileStream
        JSStdinStream
    """

    def __init__(self, string: str, error_listener: ErrorListener = None):
        """Instantiate a string stream.

        Args:
            string (str): The string with JavaScript code.
            error_listener (ErrorListener): The custom error listener. Uses default one if not set or set to None.
        """
        super().__init__(error_listener)
        self._input_stream = InputStream(string)


class JSStdinStream(JSBaseStream):
    """JavaScript stdin stream.

    See Also:
        JSBaseStream
        JSFileStream
        JSStringStream
    """

    def __init__(self, error_listener: ErrorListener = None):
        """Instantiate a string stream.

        Args:
            error_listener (ErrorListener): The custom error listener. Uses default one if not set or set to None.
        """
        super().__init__(error_listener)
        self._input_stream = StdinStream("utf-8")


class JSFileStream(JSBaseStream):
    """JavaScript file stream.

    See Also:
        JSBaseStream
        JSStringStream
        JSStdinStream
    """

    def __init__(self, path: str, error_listener: ErrorListener = None):
        """Instantiate a string stream.

        Args:
            path (str): The path to the file with JavaScript code.
            error_listener (ErrorListener): The custom error listener. Uses default one if not set or set to None.
        """
        super().__init__(error_listener)
        self._input_stream = FileStream(path)
