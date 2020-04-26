"""The module of AST nodes for expressions."""

from typing import List, Literal as TypeLiteral

from . import *
from .functions import Function
from .identifiers import Identifier
from .literals import Literal
from .operator_enums import (
    UnaryOperator,
    UpdateOperator,
    BinaryOperator,
    AssignmentOperator,
    LogicalOperator,
)
from .patterns import Pattern
from .statements import FunctionBody


class Expression(Node):
    """Any expression node. Since the left-hand side of an assignment may be any expression in general, an expression
    can also be a pattern.

    See Also:
        Pattern
    """

    def __init__(self, node_type: str, loc: Optional[SourceLocation]):
        super().__init__(node_type, loc)


class ThisExpression(Expression):
    """A `this` expression."""

    def __init__(self, loc: Optional[SourceLocation]):
        super().__init__("ThisExpression", loc)


class ArrayExpression(Expression):
    """An array expression. An element might be `None` if it represents a hole in a sparse array. E.g. ``[1,,2]``."""

    def __init__(
        self, loc: Optional[SourceLocation], elements: List[Optional[Expression]]
    ):
        super().__init__("ArrayExpression", loc)
        self.elements = elements


PropKind = TypeLiteral["init", "get", "set"]
"""A type for a `kind` field of `Property`."""


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
    ):
        super().__init__("Property", loc)
        self.key = key
        self.value = value
        self.kind = kind


class ObjectExpression(Expression):
    """An object expression."""

    def __init__(self, loc: Optional[SourceLocation], properties: List[Property]):
        super().__init__("ObjectExpression", loc)
        self.properties = properties


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


class AssignmentExpression(Expression):
    """An assignment operator expression."""

    def __init__(
        self,
        loc: Optional[SourceLocation],
        operator: AssignmentOperator,
        left: Union[Pattern, Expression],
        right: Expression,
    ):
        super().__init__("AssignmentExpression", loc)
        self.operator = operator
        self.left = left
        self.right = right


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


class UnaryMinusExpression(UnaryExpression):
    """A unary minus expression."""

    def __init__(self, loc: Optional[SourceLocation], argument: Expression):
        super().__init__(loc, UnaryOperator.MINUS, True, argument)


class UnaryPlusExpression(UnaryExpression):
    """A unary plus expression."""

    def __init__(self, loc: Optional[SourceLocation], argument: Expression):
        super().__init__(loc, UnaryOperator.PLUS, True, argument)


class UnaryLogicNotExpression(UnaryExpression):
    """A unary logic "not" expression."""

    def __init__(self, loc: Optional[SourceLocation], argument: Expression):
        super().__init__(loc, UnaryOperator.NOT_LOGIC, True, argument)


class UnaryBitNotExpression(UnaryExpression):
    """A unary bit "not" expression."""

    def __init__(self, loc: Optional[SourceLocation], argument: Expression):
        super().__init__(loc, UnaryOperator.NOT_BIT, True, argument)


class TypeofExpression(UnaryExpression):
    """A `typeof` expression."""

    def __init__(self, loc: Optional[SourceLocation], argument: Expression):
        super().__init__(loc, UnaryOperator.TYPEOF, True, argument)


class VoidExpression(UnaryExpression):
    """A `void` expression."""

    def __init__(self, loc: Optional[SourceLocation], argument: Expression):
        super().__init__(loc, UnaryOperator.VOID, True, argument)


class DeleteExpression(UnaryExpression):
    """A `delete` expression."""

    def __init__(self, loc: Optional[SourceLocation], argument: Expression):
        super().__init__(loc, UnaryOperator.DELETE, True, argument)


class PreIncrementExpression(UpdateExpression):
    """A pre-increment expression."""

    def __init__(
        self, loc: Optional[SourceLocation], argument: Expression,
    ):
        super().__init__(loc, UpdateOperator.INCREMENT, argument, True)


class PostIncrementExpression(UpdateExpression):
    """A post-increment expression."""

    def __init__(
        self, loc: Optional[SourceLocation], argument: Expression,
    ):
        super().__init__(loc, UpdateOperator.INCREMENT, argument, False)


class PreDecrementExpression(UpdateExpression):
    """A pre-decrement expression."""

    def __init__(
        self, loc: Optional[SourceLocation], argument: Expression,
    ):
        super().__init__(loc, UpdateOperator.DECREMENT, argument, True)


class PostDecrementExpression(UpdateExpression):
    """A post-decrement expression."""

    def __init__(
        self, loc: Optional[SourceLocation], argument: Expression,
    ):
        super().__init__(loc, UpdateOperator.DECREMENT, argument, False)


class EqualityExpression(BinaryExpression):
    """An equality expression."""

    def __init__(
        self, loc: Optional[SourceLocation], left: Expression, right: Expression
    ):
        super().__init__(loc, BinaryOperator.EQ, left, right)


class NotEqualityExpression(BinaryExpression):
    """A "not equality" expression."""

    def __init__(
        self, loc: Optional[SourceLocation], left: Expression, right: Expression
    ):
        super().__init__(loc, BinaryOperator.NEQ, left, right)


class IdentityEqualityExpression(BinaryExpression):
    """An identity equality expression."""

    def __init__(
        self, loc: Optional[SourceLocation], left: Expression, right: Expression
    ):
        super().__init__(loc, BinaryOperator.EQ_IDENTITY, left, right)


class NotIdentityEqualityExpression(BinaryExpression):
    """A "not identity equality" expression."""

    def __init__(
        self, loc: Optional[SourceLocation], left: Expression, right: Expression
    ):
        super().__init__(loc, BinaryOperator.NEQ_IDENTITY, left, right)


class LowerThanRelationExpression(BinaryExpression):
    """A "lower than" expression."""

    def __init__(
        self, loc: Optional[SourceLocation], left: Expression, right: Expression
    ):
        super().__init__(loc, BinaryOperator.LT, left, right)


class LowerThanEqualRelationExpression(BinaryExpression):
    """A "lower than or equal" expression."""

    def __init__(
        self, loc: Optional[SourceLocation], left: Expression, right: Expression
    ):
        super().__init__(loc, BinaryOperator.LTE, left, right)


class GreaterThanRelationExpression(BinaryExpression):
    """A "greater than" expression."""

    def __init__(
        self, loc: Optional[SourceLocation], left: Expression, right: Expression
    ):
        super().__init__(loc, BinaryOperator.GT, left, right)


class GreaterThanEqualRelationExpression(BinaryExpression):
    """A "greater than or equal" expression."""

    def __init__(
        self, loc: Optional[SourceLocation], left: Expression, right: Expression
    ):
        super().__init__(loc, BinaryOperator.GTE, left, right)


class LeftBitShiftExpression(BinaryExpression):
    """A "left bit shift" expression."""

    def __init__(
        self, loc: Optional[SourceLocation], left: Expression, right: Expression
    ):
        super().__init__(loc, BinaryOperator.SHL, left, right)


class RightBitShiftExpression(BinaryExpression):
    """A "right bit shift" expression."""

    def __init__(
        self, loc: Optional[SourceLocation], left: Expression, right: Expression
    ):
        super().__init__(loc, BinaryOperator.SHR, left, right)


class LogicRightBitShiftExpression(BinaryExpression):
    """A "logical right bit shift" expression."""

    def __init__(
        self, loc: Optional[SourceLocation], left: Expression, right: Expression
    ):
        super().__init__(loc, BinaryOperator.SHR_LOGIC, left, right)


class AddArithmeticExpression(BinaryExpression):
    """An addition arithmetical expression."""

    def __init__(
        self, loc: Optional[SourceLocation], left: Expression, right: Expression
    ):
        super().__init__(loc, BinaryOperator.ADD, left, right)


class SubArithmeticExpression(BinaryExpression):
    """A subtraction arithmetical expression."""

    def __init__(
        self, loc: Optional[SourceLocation], left: Expression, right: Expression
    ):
        super().__init__(loc, BinaryOperator.SUB, left, right)


class MulArithmeticExpression(BinaryExpression):
    """A multiplication arithmetical expression."""

    def __init__(
        self, loc: Optional[SourceLocation], left: Expression, right: Expression
    ):
        super().__init__(loc, BinaryOperator.MUL, left, right)


class DivArithmeticExpression(BinaryExpression):
    """A division arithmetical expression."""

    def __init__(
        self, loc: Optional[SourceLocation], left: Expression, right: Expression
    ):
        super().__init__(loc, BinaryOperator.DIV, left, right)


class ModArithmeticExpression(BinaryExpression):
    """A modulo arithmetical expression."""

    def __init__(
        self, loc: Optional[SourceLocation], left: Expression, right: Expression
    ):
        super().__init__(loc, BinaryOperator.MOD, left, right)


class OrBitExpression(BinaryExpression):
    """An "or" bit expression."""

    def __init__(
        self, loc: Optional[SourceLocation], left: Expression, right: Expression
    ):
        super().__init__(loc, BinaryOperator.OR, left, right)


class XorBitExpression(BinaryExpression):
    """A "xor" bit expression."""

    def __init__(
        self, loc: Optional[SourceLocation], left: Expression, right: Expression
    ):
        super().__init__(loc, BinaryOperator.XOR, left, right)


class AndBitExpression(BinaryExpression):
    """An "and" bit expression."""

    def __init__(
        self, loc: Optional[SourceLocation], left: Expression, right: Expression
    ):
        super().__init__(loc, BinaryOperator.AND, left, right)


class InExpression(BinaryExpression):
    """An "in" expression."""

    def __init__(
        self, loc: Optional[SourceLocation], left: Expression, right: Expression
    ):
        super().__init__(loc, BinaryOperator.IN, left, right)


class InstanceofExpression(BinaryExpression):
    """An "instanceof" expression."""

    def __init__(
        self, loc: Optional[SourceLocation], left: Expression, right: Expression
    ):
        super().__init__(loc, BinaryOperator.INSTANCEOF, left, right)


class SimpleAssignExpression(AssignmentExpression):
    """An assignment done with operator ``=`` expression."""

    def __init__(
        self,
        loc: Optional[SourceLocation],
        left: Union[Pattern, Expression],
        right: Expression,
    ):
        super().__init__(loc, AssignmentOperator.ASSIGN, left, right)


class AddAssignExpression(AssignmentExpression):
    """An addition assignment done with operator ``+=`` expression."""

    def __init__(
        self,
        loc: Optional[SourceLocation],
        left: Union[Pattern, Expression],
        right: Expression,
    ):
        super().__init__(loc, AssignmentOperator.ADD, left, right)


class SubAssignExpression(AssignmentExpression):
    """A subtraction assignment done with operator ``-=`` expression."""

    def __init__(
        self,
        loc: Optional[SourceLocation],
        left: Union[Pattern, Expression],
        right: Expression,
    ):
        super().__init__(loc, AssignmentOperator.SUB, left, right)


class MulAssignExpression(AssignmentExpression):
    """A multiplication assignment done with operator ``*=`` expression."""

    def __init__(
        self,
        loc: Optional[SourceLocation],
        left: Union[Pattern, Expression],
        right: Expression,
    ):
        super().__init__(loc, AssignmentOperator.MUL, left, right)


class ModAssignExpression(AssignmentExpression):
    """A modulo assignment done with operator ``%=`` expression."""

    def __init__(
        self,
        loc: Optional[SourceLocation],
        left: Union[Pattern, Expression],
        right: Expression,
    ):
        super().__init__(loc, AssignmentOperator.MOD, left, right)


class ShlAssignExpression(AssignmentExpression):
    """A left shift assignment done with operator ``<<=`` expression."""

    def __init__(
        self,
        loc: Optional[SourceLocation],
        left: Union[Pattern, Expression],
        right: Expression,
    ):
        super().__init__(loc, AssignmentOperator.SHL, left, right)


class ShrAssignExpression(AssignmentExpression):
    """A right shift assignment done with operator ``>>=`` expression."""

    def __init__(
        self,
        loc: Optional[SourceLocation],
        left: Union[Pattern, Expression],
        right: Expression,
    ):
        super().__init__(loc, AssignmentOperator.SHR, left, right)


class LogicShrAssignExpression(AssignmentExpression):
    """A logical right shift assignment done with operator ``>>>=`` expression."""

    def __init__(
        self,
        loc: Optional[SourceLocation],
        left: Union[Pattern, Expression],
        right: Expression,
    ):
        super().__init__(loc, AssignmentOperator.SHR_LOGIC, left, right)


class OrAssignExpression(AssignmentExpression):
    """A "bit or" assignment done with operator ``|=`` expression."""

    def __init__(
        self,
        loc: Optional[SourceLocation],
        left: Union[Pattern, Expression],
        right: Expression,
    ):
        super().__init__(loc, AssignmentOperator.OR, left, right)


class XorAssignExpression(AssignmentExpression):
    """A "bit xor" assignment done with operator ``^=`` expression."""

    def __init__(
        self,
        loc: Optional[SourceLocation],
        left: Union[Pattern, Expression],
        right: Expression,
    ):
        super().__init__(loc, AssignmentOperator.XOR, left, right)


class AndAssignExpression(AssignmentExpression):
    """A "bit and" assignment done with operator ``&=`` expression."""

    def __init__(
        self,
        loc: Optional[SourceLocation],
        left: Union[Pattern, Expression],
        right: Expression,
    ):
        super().__init__(loc, AssignmentOperator.AND, left, right)


class OrLogicExpression(LogicalExpression):
    """An "or" logical expression."""

    def __init__(
        self,
        loc: Optional[SourceLocation],
        left: Union[Pattern, Expression],
        right: Expression,
    ):
        super().__init__(loc, LogicalOperator.OR, left, right)


class AndLogicExpression(LogicalExpression):
    """An "and" logical expression."""

    def __init__(
        self,
        loc: Optional[SourceLocation],
        left: Union[Pattern, Expression],
        right: Expression,
    ):
        super().__init__(loc, LogicalOperator.AND, left, right)


class MemberExpression(Expression, Pattern):
    """A member expression. If `computed` is ``True``, the node corresponds to a computed (``a[b]``) member
    expression and `property` is an `Expression`. If `computed` is `False`, the node corresponds to a static
    (``a.b``) member expression and `property` is an `Identifier`. """

    def __init__(
        self,
        loc: Optional[SourceLocation],
        member_object: Expression,
        member_property: Expression,
        computed: bool,
    ):
        super().__init__("MemberExpression", loc)
        self.object = member_object
        self.property = member_property
        self.computed = computed


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


class CallExpression(Expression):
    """A function or method call expression."""

    def __init__(
        self,
        loc: Optional[SourceLocation],
        callee: Expression,
        arguments: List[Expression],
    ):
        super().__init__("CallExpression", loc)
        self.callee = callee
        self.arguments = arguments


class NewExpression(Expression):
    """A ``new`` expression."""

    def __init__(
        self,
        loc: Optional[SourceLocation],
        callee: Expression,
        arguments: List[Expression],
    ):
        super().__init__("NewExpression", loc)
        self.callee = callee
        self.arguments = arguments


class SequenceExpression(Expression):
    """A sequence expression, i.e., a comma-separated sequence of expressions."""

    def __init__(self, loc: Optional[SourceLocation], expressions: List[Expression]):
        super().__init__("SequenceExpression", loc)
        self.expressions = expressions
