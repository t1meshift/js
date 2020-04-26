"""The module of AST nodes for functions."""

from typing import List

from . import *
from .identifiers import Identifier
from .patterns import Pattern
from .statements import FunctionBody


class Function(Node):
    """A function declaration or expression.

    See Also:
        FunctionDeclaration
        FunctionExpression
        FunctionBody
    """

    def __init__(
        self,
        node_type: str,
        loc: Optional[SourceLocation],
        function_id: Optional[Identifier],
        params: List[Pattern],
        body: FunctionBody,
    ):
        super().__init__(node_type, loc)
        self.id = function_id
        self.params = params
        self.body = body
