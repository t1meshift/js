"""The module of AST nodes for declarations."""

from typing import List

from . import *
from .identifiers import Identifier
from .patterns import Pattern
from .statements import Statement, FunctionBody
from .functions import Function


class Declaration(Statement):
    """Any declaration node. Note that declarations are considered statements; this is because declarations can
    appear in any statement context. """

    def __init__(self, node_type: str, loc: Optional[SourceLocation]):
        super().__init__(node_type, loc)


class FunctionDeclaration(Function, Declaration):
    """A function declaration. Note that unlike in the parent interface `Function`, the `id` cannot be `None`."""

    def __init__(
        self,
        loc: Optional[SourceLocation],
        function_id: Identifier,
        params: List[Pattern],
        body: FunctionBody,
    ):
        super().__init__("FunctionDeclaration", loc, function_id, params, body)


class VariableDeclarator(Node):
    """A variable declarator."""

    def __init__(
        self, loc: Optional[SourceLocation], var_id: Pattern, init: Optional[Exception]
    ):
        super().__init__("VariableDeclarator", loc)
        self.id = var_id
        self.init = init


class VariableDeclaration(Declaration):
    """A variable declaration."""

    def __init__(
        self, loc: Optional[SourceLocation], declarations: List[VariableDeclarator]
    ):
        super().__init__("VariableDeclaration", loc)
        self.declarations = declarations
        self.kind = "var"
