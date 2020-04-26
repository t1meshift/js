"""The module representing enums for JavaScript operators."""

from enum import Enum


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
