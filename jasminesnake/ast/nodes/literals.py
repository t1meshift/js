"""The module of AST nodes for literals."""

from . import *
from .expressions import Expression


class Literal(Expression):
    """A literal token. Note that a literal can be an expression."""

    def __init__(
        self, loc: Optional[SourceLocation], value: Union[str, bool, number, None]
    ):
        super().__init__("Literal", loc)
        self.value = value
