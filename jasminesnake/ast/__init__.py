"""AST module."""

from enum import Enum
from typing import Union
from antlr4 import ParseTreeWalker

import lex.JavaScriptParser as Parser
import ast.nodes
from .parse_tree_listeners import ASTListener

JSP = Parser.JavaScriptParser


def from_parse_tree(tree: JSP.ProgramContext) -> ast.nodes.Program:
    """Generate AST from ANTLR parse tree.

    Args:
        tree (JSP.ProgramContext): ANTLR parse tree.

    Returns:
        `Program` AST node, which is the root node.
    """
    ast_listener = ASTListener()
    ParseTreeWalker.DEFAULT.walk(ast_listener, tree)
    return ast_listener.program_node


def to_ascii_tree(
    node: Union[ast.nodes.Position, ast.nodes.SourceLocation, ast.nodes.Node],
    name_prefix: str = "",
    nesting_lvl: int = 0,
):
    if nesting_lvl < 0:
        raise ValueError("Nesting level can't be below 0")

    FORK = "+"
    VERTICAL = "|"
    HORIZONTAL = "-"

    SUBENTRY_PREFIX = f"{FORK}{HORIZONTAL}{HORIZONTAL} "
    NESTED_PREFIX = f"{VERTICAL}   "

    value = str(node)
    children = None

    if isinstance(node, Enum):
        value = str(node.value)

    if isinstance(node, list):
        value = ""
        children = [(index, val) for index, val in enumerate(node)]

    if hasattr(node, "fields"):
        children = [(k, node.fields[k]) for k in node.fields.keys()]

    result = f"{NESTED_PREFIX * (nesting_lvl - 1)}{SUBENTRY_PREFIX * (nesting_lvl > 0)}"
    result += f"{name_prefix}{value}\n"

    if children is not None:
        for (child_name, child_value) in children:
            result += to_ascii_tree(child_value, f"{child_name}: ", nesting_lvl + 1)

        # result += "\n"

    return result


# Delete temporary imports
del JSP
del Parser
