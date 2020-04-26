"""The module of Program AST node."""

from typing import List
from . import *
from .statements import Statement, Directive


class Program(Node):
    """A complete program source tree."""

    def __init__(
        self, loc: Optional[SourceLocation], body: List[Union[Directive, Statement]]
    ):
        super().__init__("Program", loc)
        self.body = body
