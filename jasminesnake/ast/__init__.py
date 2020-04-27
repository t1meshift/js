"""AST module."""

from antlr4 import ParseTreeWalker
from tree_format import format_tree

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


# Delete temporary imports
del JSP
del Parser
