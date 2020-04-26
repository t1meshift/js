"""The module of AST nodes for statements."""

from typing import List

from . import *
from .expressions import Expression
from .literals import Literal
from .identifiers import Identifier
from .declarations import VariableDeclaration
from .patterns import Pattern


class Statement(Node):
    """Any statement."""

    def __init__(self, node_type: str, loc: Optional[SourceLocation]):
        super().__init__(node_type, loc)


class EmptyStatement(Statement):
    """An empty statement, i.e., a solitary semicolon."""

    def __init__(self, loc: Optional[SourceLocation]):
        super().__init__("EmptyStatement", loc)


class BlockStatement(Statement):
    """A block statement, i.e., a sequence of statements surrounded by braces."""

    def __init__(self, loc: Optional[SourceLocation], body: List[Statement]):
        super().__init__("BlockStatement", loc)
        self.body = body


class ExpressionStatement(Statement):
    """An expression statement, i.e., a statement consisting of a single expression."""

    def __init__(self, loc: Optional[SourceLocation], expression: Expression):
        super().__init__("ExpressionStatement", loc)
        self.expression = expression


class Directive(Node):
    """A directive from the directive prologue of a script or function. The `directive` property is the raw string
    source of the directive without quotes.
    """

    def __init__(
        self, loc: Optional[SourceLocation], expression: Literal, directive: str
    ):
        super().__init__("Directive", loc)
        self.expression = expression
        self.directive = directive


class FunctionBody(BlockStatement):
    """The body of a function, which is a block statement that may begin with directives."""

    def __init__(
        self, loc: Optional[SourceLocation], body: List[Union[Directive, Statement]]
    ):
        super().__init__(loc, body)


class ReturnStatement(Statement):
    """A `return` statement."""

    def __init__(self, loc: Optional[SourceLocation], argument: Optional[Expression]):
        super().__init__("ReturnStatement", loc)
        self.argument = argument


class BreakStatement(Statement):
    """A `break` statement."""

    def __init__(self, loc: Optional[SourceLocation], label: Optional[Identifier]):
        super().__init__("BreakStatement", loc)
        self.label = label


class ContinueStatement(Statement):
    """A `continue` statement."""

    def __init__(self, loc: Optional[SourceLocation], label: Optional[Identifier]):
        super().__init__("ContinueStatement", loc)
        self.label = label


class IfStatement(Statement):
    """An `if` statement."""

    def __init__(
        self,
        loc: Optional[SourceLocation],
        test: Expression,
        consequent: Statement,
        alternate: Optional[Statement],
    ):
        super().__init__("IfStatement", loc)
        self.test = test
        self.consequent = consequent
        self.alternate = alternate


class WhileStatement(Statement):
    """A `while` statement."""

    def __init__(
        self, loc: Optional[SourceLocation], test: Expression, body: Statement
    ):
        super().__init__("WhileStatement", loc)
        self.test = test
        self.body = body


class DoWhileStatement(Statement):
    """A `do`/`while` statement."""

    def __init__(
        self, loc: Optional[SourceLocation], body: Statement, test: Expression
    ):
        super().__init__("DoWhileStatement", loc)
        self.body = body
        self.test = test


class ForStatement(Statement):
    """A `for` statement."""

    def __init__(
        self,
        loc: Optional[SourceLocation],
        init: Union[VariableDeclaration, Expression, None],
        test: Optional[Expression],
        update: Optional[Expression],
        body: Statement,
    ):
        super().__init__("ForStatement", loc)
        self.init = init
        self.test = test
        self.update = update
        self.body = body


class ForInStatement(Statement):
    """A `for`/`in` statement."""

    def __init__(
        self,
        loc: Optional[SourceLocation],
        left: Union[VariableDeclaration, Pattern],
        right: Expression,
        body: Statement,
    ):
        super().__init__("ForInStatement", loc)
        self.left = left
        self.right = right
        self.body = body
