"""The module with AST nodes declaration. They are ESTree compliant.

The module lacks support of:
 * ES5 features:
    * labelled statements
    * switch statements
    * try-catch statements
    * debugger statement
    * with statement
    * RegExp
 * ES6 features:
    * generators/yield statement
    * for-of statement
    * template literals
    * and other ES6 features :)

More about ESTree standard:
https://github.com/estree/estree/

Todo:
    * Add support for lacking features
"""

from typing import List, Union, Optional, Literal as TypeLiteral, TypedDict, Any
from enum import Enum
from collections import OrderedDict

# The Lord sees I actually wanted to split it up, but ESTree hierarchy is so messed up... No. It's actually *fucked up*
# that much that I couldn't even resolve circular dependencies in the submodules. I have to reap what I've sown.

# Custom types used in the nodes

number = Union[int, float]
"""A type union consisting of int and float Python types. Consider it as Number type from JavaScript."""

SourceTypeLiteral = TypeLiteral["script", "module"]
"""The type for the `sourceType` field."""

VarDeclKind = TypeLiteral["var", "let", "const"]
"""The type for the `kind` field of `VariableDeclaration`."""

PropKind = TypeLiteral["init", "get", "set"]
"""A type for a `kind` field of `Property`."""


class UnaryOperator(Enum):
    """A unary operator token."""

    MINUS = "-"
    PLUS = "+"
    NOT_LOGIC = "!"
    NOT_BIT = "~"
    TYPEOF = "typeof"
    VOID = "void"
    DELETE = "delete"


class UpdateOperator(Enum):
    """An update (increment or decrement) operator token."""

    INCREMENT = "++"
    DECREMENT = "--"


class BinaryOperator(Enum):
    """A binary operator token."""

    EQ = "=="
    NEQ = "!="
    EQ_IDENTITY = "==="
    NEQ_IDENTITY = "!=="
    LT = "<"
    LTE = "<="
    GT = ">"
    GTE = ">="
    SHL = "<<"
    SHR = ">>"
    SHR_LOGIC = ">>>"
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"
    MOD = "%"
    OR = "|"
    XOR = "^"
    AND = "&"
    IN = "in"
    INSTANCEOF = "instanceof"


class AssignmentOperator(Enum):
    """An assignment operator token."""

    ASSIGN = "="
    ADD = "+="
    SUB = "-="
    MUL = "*="
    DIV = "/="
    MOD = "%="
    SHL = "<<="
    SHR = ">>="
    SHR_LOGIC = ">>>="
    OR = "|="
    XOR = "^="
    AND = "&="


class LogicalOperator(Enum):
    """A logical operator token."""

    OR = "||"
    AND = "&&"


# Nodes forward declarations
class Expression:
    ...


class Pattern:
    ...


class Directive:
    ...


class Statement:
    ...


class FunctionBody:
    ...


class VariableDeclaration:
    ...


class Property:
    ...


class Identifier:
    ...


# "Node objects" block


class Position:
    """The class for an object consisting of a line number (1-indexed) and a column number (0-indexed)."""

    def __init__(self, line: int, column: int):
        if line < 1 or column < 0:
            raise ValueError(
                "L{}:C{} is not valid ESTree position!".format(line, column)
            )

        self.line = line
        self.column = column

    def __str__(self):
        return f"{self.line}:{self.column}"


class SourceLocation:
    """
    The class for the source location information of a node.

    Consists of a start position (the position of the first character of the parsed source region) and an end
    position (the position of the first character after the parsed source region).

    See Also:
        Position
    """

    def __init__(self, source: Optional[str], start: Position, end: Position):
        self.source = source
        self.start = start
        self.end = end

    @property
    def fields(self):
        return OrderedDict({"start": self.start, "end": self.end})

    def __str__(self):
        src = "" if self.source is None else f"{self.source}:"
        return f"{src}{str(self.start)}"


class Node:
    """ESTree AST nodes are represented as Node objects, which may have any prototype inheritance but which implement
    this interface.

    The `type` field is a string representing the AST variant type. Each subtype of `Node` is documented below with
    the specific string of its `type` field. You can use this field to determine which interface a node implements.

    The `loc` field represents the source location information of the node. If the node contains no information about
    the source location, the field is `None`; otherwise it contains a `SourceLocation` object.

    See Also:
        SourceLocation
    """

    def __init__(self, node_type: str, loc: Optional[SourceLocation]):
        self.type = node_type
        self.loc = loc

        self._fields: OrderedDict[str, Any] = OrderedDict()
        self._fields.update({"type": self.type, "loc": self.loc})

    def __str__(self):
        return f"{self.type} at {str(self.loc)}"

    @property
    def fields(self):
        return self._fields


# "Literal" block


class Literal(Expression):
    """A literal token. Note that a literal can be an expression."""

    def __init__(
        self, loc: Optional[SourceLocation], value: Union[str, bool, number, None]
    ):
        super().__init__("Literal", loc)
        self.value = value
        self._fields.update({"value": self.value})


# "Programs" block


class Program(Node):
    """A complete program source tree."""

    def __init__(
        self,
        loc: Optional[SourceLocation],
        source_type: SourceTypeLiteral,
        body: List[Union[Directive, Statement]],
    ):
        super().__init__("Program", loc)
        self.body = body
        self.source_type = source_type
        self._fields.update({"sourceType": self.source_type, "body": self.body})


# "Functions" block


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
        self._fields.update({"id": self.id, "params": self.params, "body": self.body})


# "Statements" block


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
        self._fields.update({"body": self.body})


class ExpressionStatement(Statement):
    """An expression statement, i.e., a statement consisting of a single expression."""

    def __init__(self, loc: Optional[SourceLocation], expression: Expression):
        super().__init__("ExpressionStatement", loc)
        self.expression = expression
        self._fields.update({"expression": self.expression})


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
        self._fields.update(
            {"expression": self.expression, "directive": self.directive}
        )


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
        self._fields.update({"argument": self.argument})


class BreakStatement(Statement):
    """A `break` statement."""

    def __init__(self, loc: Optional[SourceLocation], label: Optional[Identifier]):
        super().__init__("BreakStatement", loc)
        self.label = label
        self._fields.update({"label": self.label})


class ContinueStatement(Statement):
    """A `continue` statement."""

    def __init__(self, loc: Optional[SourceLocation], label: Optional[Identifier]):
        super().__init__("ContinueStatement", loc)
        self.label = label
        self._fields.update({"label": self.label})


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
        self._fields.update(
            {
                "test": self.test,
                "consequent": self.consequent,
                "alternate": self.alternate,
            }
        )


class WhileStatement(Statement):
    """A `while` statement."""

    def __init__(
        self, loc: Optional[SourceLocation], test: Expression, body: Statement
    ):
        super().__init__("WhileStatement", loc)
        self.test = test
        self.body = body
        self._fields.update({"test": self.test, "body": self.body})


class DoWhileStatement(Statement):
    """A `do`/`while` statement."""

    def __init__(
        self, loc: Optional[SourceLocation], body: Statement, test: Expression
    ):
        super().__init__("DoWhileStatement", loc)
        self.body = body
        self.test = test
        self._fields.update({"body": self.body, "test": self.test})


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
        self._fields.update(
            {
                "init": self.init,
                "test": self.test,
                "update": self.update,
                "body": self.body,
            }
        )


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
        self._fields.update({"left": self.left, "right": self.right, "body": self.body})


# "Declarations" block


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
        self, loc: Optional[SourceLocation], var_id: Pattern, init: Optional[Expression]
    ):
        super().__init__("VariableDeclarator", loc)
        self.id = var_id
        self.init = init
        self._fields.update({"id": self.id, "init": self.init})


class VariableDeclaration(Declaration):
    """A variable declaration."""

    def __init__(
        self,
        loc: Optional[SourceLocation],
        kind: VarDeclKind,
        declarations: List[VariableDeclarator],
    ):
        super().__init__("VariableDeclaration", loc)
        self.declarations = declarations
        self.kind = kind
        self._fields.update({"kind": self.kind, "declarations": self.declarations})


# "Expressions" block


class Expression(Node):
    """Any expression node. Since the left-hand side of an assignment may be any expression in general, an expression
    can also be a pattern.

    See Also:
        Pattern
    """

    def __init__(self, node_type: str, loc: Optional[SourceLocation]):
        super().__init__(node_type, loc)


class Super(Node):
    """A ``super`` pseudo-expression."""

    def __init__(self, loc: Optional[SourceLocation]):
        super().__init__("Super", loc)


class SpreadElement(Node):
    """Spread expression, e.g., ``[head, ...iter, tail]``, ``f(head, ...iter, ...tail)``."""

    def __init__(self, loc: Optional[SourceLocation], argument: Expression):
        super().__init__("SpreadElement", loc)
        self.argument = argument
        self._fields.update({"argument": self.argument})


class ThisExpression(Expression):
    """A `this` expression."""

    def __init__(self, loc: Optional[SourceLocation]):
        super().__init__("ThisExpression", loc)


class ArrayExpression(Expression):
    """An array expression. An element might be `None` if it represents a hole in a sparse array. E.g. ``[1,,2]``."""

    def __init__(
        self,
        loc: Optional[SourceLocation],
        elements: List[Union[Expression, SpreadElement, None]],
    ):
        super().__init__("ArrayExpression", loc)
        self.elements = elements
        self._fields.update({"elements": self.elements})


class ObjectExpression(Expression):
    """An object expression."""

    def __init__(self, loc: Optional[SourceLocation], properties: List[Property]):
        super().__init__("ObjectExpression", loc)
        self.properties = properties
        self._fields.update({"properties": self.properties})


class FunctionExpression(Function, Expression):
    """A function expression."""

    def __init__(
        self,
        loc: Optional[SourceLocation],
        function_id: Optional[Identifier],
        params: List[Pattern],
        body: FunctionBody,
    ):
        super().__init__("FunctionExpression", loc, function_id, params, body)


class ArrowFunctionExpression(Function, Expression):
    """A fat arrow function expression, e.g., ``let foo = (bar) => { /* body */ }``."""

    def __init__(
        self,
        loc: Optional[SourceLocation],
        params: List[Pattern],
        body: Union[FunctionBody, Expression],
        expression: bool,
    ):
        super().__init__("ArrowFunctionExpression", loc, None, params, body)
        self.expression = expression
        self._fields.update({"expression": self.expression})


class UnaryExpression(Expression):
    """A unary operator expression."""

    def __init__(
        self,
        loc: Optional[SourceLocation],
        operator: UnaryOperator,
        prefix: bool,
        argument: Expression,
    ):
        super().__init__("UnaryExpression", loc)
        self.operator = operator
        self.prefix = prefix
        self.argument = argument
        self._fields.update(
            {
                "operator": self.operator,
                "prefix": self.prefix,
                "argument": self.argument,
            }
        )


class UpdateExpression(Expression):
    """An update (increment or decrement) operator expression."""

    def __init__(
        self,
        loc: Optional[SourceLocation],
        operator: UpdateOperator,
        argument: Expression,
        prefix: bool,
    ):
        super().__init__("UpdateExpression", loc)
        self.operator = operator
        self.argument = argument
        self.prefix = prefix
        self._fields.update(
            {
                "operator": self.operator,
                "argument": self.argument,
                "prefix": self.prefix,
            }
        )


class BinaryExpression(Expression):
    """A binary operator expression."""

    def __init__(
        self,
        loc: Optional[SourceLocation],
        operator: BinaryOperator,
        left: Expression,
        right: Expression,
    ):
        super().__init__("BinaryExpression", loc)
        self.operator = operator
        self.left = left
        self.right = right
        self._fields.update(
            {"operator": self.operator, "left": self.left, "right": self.right}
        )


class AssignmentExpression(Expression):
    """An assignment operator expression."""

    def __init__(
        self,
        loc: Optional[SourceLocation],
        operator: AssignmentOperator,
        left: Union[
            Pattern, Expression
        ],  # Left for backwards compatibility with pre-ES6 code, should be `Pattern`
        right: Expression,
    ):
        super().__init__("AssignmentExpression", loc)
        self.operator = operator
        self.left = left
        self.right = right
        self._fields.update(
            {"operator": self.operator, "left": self.left, "right": self.right}
        )


class LogicalExpression(Expression):
    """A logical operator expression."""

    def __init__(
        self,
        loc: Optional[SourceLocation],
        operator: LogicalOperator,
        left: Union[Pattern, Expression],
        right: Expression,
    ):
        super().__init__("LogicalExpression", loc)
        self.operator = operator
        self.left = left
        self.right = right
        self._fields.update(
            {"operator": self.operator, "left": self.left, "right": self.right}
        )


class MemberExpression(Expression, Pattern):
    """A member expression. If `computed` is ``True``, the node corresponds to a computed (``a[b]``) member
    expression and `property` is an `Expression`. If `computed` is `False`, the node corresponds to a static
    (``a.b``) member expression and `property` is an `Identifier`. """

    def __init__(
        self,
        loc: Optional[SourceLocation],
        member_object: Union[Expression, Super],
        member_property: Expression,
        computed: bool,
    ):
        super().__init__("MemberExpression", loc)
        self.object = member_object
        self.property = member_property
        self.computed = computed
        self._fields.update(
            {
                "object": self.object,
                "property": self.property,
                "computed": self.computed,
            }
        )


class ConditionalExpression(Expression):
    """A conditional expression, i.e., a ternary ``?``/``:`` expression."""

    def __init__(
        self,
        loc: Optional[SourceLocation],
        test: Expression,
        alternate: Expression,
        consequent: Expression,
    ):
        super().__init__("ConditionalExpression", loc)
        self.test = test
        self.alternate = alternate
        self.consequent = consequent
        self._fields.update(
            {
                "test": self.test,
                "alternate": self.alternate,
                "consequent": self.consequent,
            }
        )


class CallExpression(Expression):
    """A function or method call expression."""

    def __init__(
        self,
        loc: Optional[SourceLocation],
        callee: Union[Expression, Super],
        arguments: List[Union[Expression, SpreadElement]],
    ):
        super().__init__("CallExpression", loc)
        self.callee = callee
        self.arguments = arguments
        self._fields.update({"callee": self.callee, "arguments": self.arguments})


class NewExpression(Expression):
    """A ``new`` expression."""

    def __init__(
        self,
        loc: Optional[SourceLocation],
        callee: Expression,
        arguments: List[Union[Expression, SpreadElement]],
    ):
        super().__init__("NewExpression", loc)
        self.callee = callee
        self.arguments = arguments
        self._fields.update({"callee": self.callee, "arguments": self.arguments})


class SequenceExpression(Expression):
    """A sequence expression, i.e., a comma-separated sequence of expressions."""

    def __init__(self, loc: Optional[SourceLocation], expressions: List[Expression]):
        super().__init__("SequenceExpression", loc)
        self.expressions = expressions
        self._fields.update({"expressions": self.expressions})


def _generate_unary_expression(operator: UnaryOperator, docstring: str):
    """Internal function to generate unary expression AST node.

    Implying that all UnaryExpression nodes are prefix.
    """

    class Expr(UnaryExpression):
        __doc__ = docstring

        def __init__(self, loc: Optional[SourceLocation], argument: Expression):
            super().__init__(loc, operator, True, argument)

    return Expr


def _generate_update_expression(operator: UpdateOperator, prefix: bool, docstring: str):
    """Internal function to generate update expression AST node."""

    class Expr(UpdateExpression):
        __doc__ = docstring

        def __init__(self, loc: Optional[SourceLocation], argument: Expression):
            super().__init__(loc, operator, argument, prefix)

    return Expr


def _generate_binary_expression(operator: BinaryOperator, docstring: str):
    """Internal function to generate binary expression AST node."""

    class Expr(BinaryExpression):
        __doc__ = docstring

        def __init__(
            self, loc: Optional[SourceLocation], left: Expression, right: Expression
        ):
            super().__init__(loc, operator, left, right)

    return Expr


def _generate_assignment_expression(operator: AssignmentOperator, docstring: str):
    """Internal function to generate assignment expression AST node."""

    class Expr(AssignmentExpression):
        __doc__ = docstring

        def __init__(
            self,
            loc: Optional[SourceLocation],
            left: Union[Pattern, Expression],
            right: Expression,
        ):
            super().__init__(loc, operator, left, right)

    return Expr


def _generate_logical_expression(operator: LogicalOperator, docstring: str):
    """Internal function to generate logical expression AST node."""

    class Expr(LogicalExpression):
        __doc__ = docstring

        def __init__(
            self,
            loc: Optional[SourceLocation],
            left: Union[Pattern, Expression],
            right: Expression,
        ):
            super().__init__(loc, operator, left, right)

    return Expr


UnaryMinusExpression = _generate_unary_expression(
    UnaryOperator.MINUS, """A unary minus expression."""
)
UnaryPlusExpression = _generate_unary_expression(
    UnaryOperator.PLUS, """A unary plus expression."""
)
UnaryLogicNotExpression = _generate_unary_expression(
    UnaryOperator.NOT_LOGIC, """A unary logic "not" expression."""
)
UnaryBitNotExpression = _generate_unary_expression(
    UnaryOperator.NOT_BIT, """A unary bit "not" expression."""
)
TypeofExpression = _generate_unary_expression(
    UnaryOperator.TYPEOF, """A `typeof` expression."""
)
VoidExpression = _generate_unary_expression(
    UnaryOperator.VOID, """A `void` expression."""
)
DeleteExpression = _generate_unary_expression(
    UnaryOperator.DELETE, """A `delete` expression."""
)
PreIncrementExpression = _generate_update_expression(
    UpdateOperator.INCREMENT, True, """A pre-increment expression."""
)
PostIncrementExpression = _generate_update_expression(
    UpdateOperator.INCREMENT, False, """A post-increment expression."""
)
PreDecrementExpression = _generate_update_expression(
    UpdateOperator.DECREMENT, True, """A pre-decrement expression."""
)
PostDecrementExpression = _generate_update_expression(
    UpdateOperator.DECREMENT, False, """A post-decrement expression."""
)
EqualityExpression = _generate_binary_expression(
    BinaryOperator.EQ, """An equality expression."""
)
NotEqualityExpression = _generate_binary_expression(
    BinaryOperator.NEQ, """A "not equality" expression."""
)
IdentityEqualityExpression = _generate_binary_expression(
    BinaryOperator.EQ_IDENTITY, """An identity equality expression."""
)
NotIdentityEqualityExpression = _generate_binary_expression(
    BinaryOperator.NEQ_IDENTITY, """A "not identity equality" expression."""
)
LowerThanRelationExpression = _generate_binary_expression(
    BinaryOperator.LT, """A "lower than" expression."""
)
LowerThanEqualRelationExpression = _generate_binary_expression(
    BinaryOperator.LTE, """A "lower than or equal" expression."""
)
GreaterThanRelationExpression = _generate_binary_expression(
    BinaryOperator.GT, """A "greater than" expression."""
)
GreaterThanEqualRelationExpression = _generate_binary_expression(
    BinaryOperator.GTE, """A "greater than or equal" expression."""
)
LeftBitShiftExpression = _generate_binary_expression(
    BinaryOperator.SHL, """A "left bit shift" expression."""
)
RightBitShiftExpression = _generate_binary_expression(
    BinaryOperator.SHR, """A "right bit shift" expression."""
)
LogicRightBitShiftExpression = _generate_binary_expression(
    BinaryOperator.SHR_LOGIC, """A "logical right bit shift" expression."""
)
AddArithmeticExpression = _generate_binary_expression(
    BinaryOperator.ADD, """An addition arithmetical expression."""
)
SubArithmeticExpression = _generate_binary_expression(
    BinaryOperator.SUB, """A subtraction arithmetical expression."""
)
MulArithmeticExpression = _generate_binary_expression(
    BinaryOperator.MUL, """A multiplication arithmetical expression."""
)
DivArithmeticExpression = _generate_binary_expression(
    BinaryOperator.DIV, """A division arithmetical expression."""
)
ModArithmeticExpression = _generate_binary_expression(
    BinaryOperator.MOD, """A modulo arithmetical expression."""
)
OrBitExpression = _generate_binary_expression(
    BinaryOperator.OR, """An "or" bit expression."""
)
XorBitExpression = _generate_binary_expression(
    BinaryOperator.XOR, """A "xor" bit expression."""
)
AndBitExpression = _generate_binary_expression(
    BinaryOperator.AND, """An "and" bit expression."""
)
InExpression = _generate_binary_expression(BinaryOperator.IN, """An "in" expression.""")
InstanceofExpression = _generate_binary_expression(
    BinaryOperator.INSTANCEOF, """An "instanceof" expression."""
)
SimpleAssignExpression = _generate_assignment_expression(
    AssignmentOperator.ASSIGN, """An assignment done with operator ``=`` expression."""
)
AddAssignExpression = _generate_assignment_expression(
    AssignmentOperator.ADD,
    """An addition assignment done with operator ``+=`` expression.""",
)
SubAssignExpression = _generate_assignment_expression(
    AssignmentOperator.SUB,
    """A subtraction assignment done with operator ``-=`` expression.""",
)
MulAssignExpression = _generate_assignment_expression(
    AssignmentOperator.MUL,
    """A multiplication assignment done with operator ``*=`` expression.""",
)
ModAssignExpression = _generate_assignment_expression(
    AssignmentOperator.DIV,
    """A modulo assignment done with operator ``%=`` expression.""",
)
ShlAssignExpression = _generate_assignment_expression(
    AssignmentOperator.SHL,
    """A left shift assignment done with operator ``<<=`` expression.""",
)
ShrAssignExpression = _generate_assignment_expression(
    AssignmentOperator.SHR,
    """A right shift assignment done with operator ``>>=`` expression.""",
)
LogicShrAssignExpression = _generate_assignment_expression(
    AssignmentOperator.SHR_LOGIC,
    """A logical right shift assignment done with operator ``>>>=`` expression.""",
)
OrAssignExpression = _generate_assignment_expression(
    AssignmentOperator.OR,
    """A "bit or" assignment done with operator ``|=`` expression.""",
)
XorAssignExpression = _generate_assignment_expression(
    AssignmentOperator.XOR,
    """A "bit xor" assignment done with operator ``^=`` expression.""",
)
AndAssignExpression = _generate_assignment_expression(
    AssignmentOperator.AND,
    """A "bit and" assignment done with operator ``&=`` expression.""",
)
OrLogicExpression = _generate_logical_expression(
    LogicalOperator.OR, """An "or" logical expression."""
)
AndLogicExpression = _generate_logical_expression(
    LogicalOperator.AND, """An "and" logical expression."""
)


# "Property" block


class Property(Node):
    """A literal property in an object expression can have either a string or number as its `value`. Ordinary
    property initializers have a `kind` value ``"init"``; getters and setters have the kind values ``"get"`` and
    ``"set"``, respectively. """

    def __init__(
        self,
        loc: Optional[SourceLocation],
        key: Union[Literal, Identifier],
        value: Expression,
        kind: PropKind,
        method: bool,
        shorthand: bool,
        computed: bool,
    ):
        super().__init__("Property", loc)
        self.key = key
        self.value = value
        self.kind = kind
        self.method = method
        self.shorthand = shorthand
        self.computed = computed
        self._fields.update(
            {
                "key": self.key,
                "value": self.value,
                "kind": self.kind,
                "method": self.method,
                "shorthand": self.shorthand,
                "computed": self.computed,
            }
        )


class AssignmentProperty(Property):
    def __init__(
        self,
        loc: Optional[SourceLocation],
        key: Union[Literal, Identifier],
        value: Pattern,
        shorthand: bool,
        computed: bool,
    ):
        super().__init__(loc, key, value, "init", False, shorthand, computed)


# "Patterns" block
#
# Destructuring binding and assignment are not part of ES5, but all binding positions accept Pattern
# to allow for destructuring in ES6. Nevertheless, for ES5, the only Pattern subtype is Identifier.


class Pattern(Node):
    """A pattern."""

    def __init__(self, node_type: str, loc: Optional[SourceLocation]):
        super().__init__(node_type, loc)


class ObjectPatternKeyValue(TypedDict):
    key: Union[Literal, Identifier]
    value: Pattern


class ObjectPattern(Pattern):
    def __init__(
        self, loc: Optional[SourceLocation], properties: List[ObjectPatternKeyValue]
    ):
        super().__init__("ObjectPattern", loc)
        self.properties = properties
        self._fields.update({"properties": self.properties})


class ArrayPattern(Pattern):
    def __init__(
        self, loc: Optional[SourceLocation], elements: List[Optional[Pattern]]
    ):
        super().__init__("ArrayPattern", loc)
        self.elements = elements
        self._fields.update({"elements": self.elements})


# "Identifier" block


class Identifier(Expression, Pattern):
    """An identifier. Note that an identifier may be an expression or a destructuring pattern."""

    def __init__(self, loc: Optional[SourceLocation], name: str):
        super().__init__("Identifier", loc)
        self.name = name
        self._fields.update({"name": self.name})
