"""The module with AST nodes declaration. They are ESTree compliant.

The module lacks support of:
 * ES5 features:
    * labelled statements
    * switch statements
    * try-catch statements
    * debugger statement
    * with statement
    * RegExp
 * ES6+

More about ESTree standard:
https://github.com/estree/estree/

Todo:
    * Add support for lacking features
"""

from typing import Optional, Union


class Position:
    """The class for an object consisting of a line number (1-indexed) and a column number (0-indexed)."""

    def __init__(self, line: int, column: int):
        if line < 1 or column < 0:
            raise ValueError(
                "L{}:C{} is not valid ESTree position!".format(line, column)
            )

        self.line = line
        self.column = column


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


number = Union[int, float]
"""A type union consisting of int and float Python types. Consider it as Number type from JavaScript."""
