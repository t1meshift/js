"""The module of AST nodes for identifiers."""

from . import *
from .patterns import Pattern
from .expressions import Expression


class Identifier(Expression, Pattern):
    """An identifier. Note that an identifier may be an expression or a destructuring pattern."""

    def __init__(self, loc: Optional[SourceLocation], name: str):
        super(Identifier, self).__init__("Identifier", loc)
        self.name = name
