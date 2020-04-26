"""The module of AST nodes for patterns.

Destructuring binding and assignment are not part of ES5, but all binding positions accept `Pattern` to allow for
destructuring in ES6. Nevertheless, for ES5, the only `Pattern` subtype is `Identifier`.

See Also:
    Identifier
"""

from typing import TypedDict, Union, List
from . import *
from .literals import Literal
from .identifiers import Identifier


class Pattern(Node):
    """A pattern."""

    def __init__(self, node_type: str, loc: Optional[SourceLocation]):
        super().__init__(node_type, loc)


class ObjectKeyValue(TypedDict):
    key: Union[Literal, Identifier]
    value: Pattern


class ObjectPattern(Pattern):
    def __init__(self, loc: Optional[SourceLocation], properties: List[ObjectKeyValue]):
        super().__init__("ObjectPattern", loc)
        self.properties = properties


class ArrayPattern(Pattern):
    def __init__(
        self, loc: Optional[SourceLocation], elements: List[Optional[Pattern]]
    ):
        super().__init__("ArrayPattern", loc)
        self.elements = elements
