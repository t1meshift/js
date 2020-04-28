import logging
from typing import Optional, List, Union
import antlr4.ParserRuleContext

from ..lex.JavaScriptParser import JavaScriptParser
from ..lex.JavaScriptParserListener import JavaScriptParserListener as JSBaseListener

from . import nodes


def _get_source_location(
    ctx: antlr4.ParserRuleContext, source: Optional[str]
) -> nodes.SourceLocation:
    """Internal function to obtain `SourceObject` from parser context."""
    start_pos = nodes.Position(ctx.start.line, ctx.start.column)
    end_pos = nodes.Position(ctx.stop.line, ctx.stop.column)

    # If an end is not on a newline, shift end position column by 1
    # to match exact token end, not the last character
    if end_pos.column != 0:
        end_pos.column += 1

    return nodes.SourceLocation(source=source, start=start_pos, end=end_pos)


class AssignableListener(JSBaseListener):
    _result: Union[nodes.Identifier, nodes.ObjectPattern, nodes.ArrayPattern]

    @property
    def result(self):
        return self._result

    def enterAssignable(self, ctx: JavaScriptParser.AssignableContext):
        logging.debug("Entered section Assignable")
        ctx.getChild(0).enterRule(self)

    def enterIdentifier(self, ctx: JavaScriptParser.IdentifierContext):
        logging.debug("Entered section Identifier")
        loc = _get_source_location(ctx, None)
        self._result = nodes.Identifier(loc, ctx.getText())

    def enterArrayLiteral(self, ctx: JavaScriptParser.ArrayLiteralContext):
        logging.debug("Entered section ArrayLiteral")
        pass  # TODO

    def enterObjectLiteral(self, ctx: JavaScriptParser.ObjectLiteralContext):
        logging.debug("Entered section ObjectLiteral")
        pass  # TODO


class VariableDeclarationListener(JSBaseListener):
    _var_decl: nodes.VariableDeclarator

    @property
    def var_declarator(self):
        return self._var_decl

    def enterVariableDeclaration(
        self, ctx: JavaScriptParser.VariableDeclarationContext
    ):
        loc = _get_source_location(ctx, None)
        assign_listener = AssignableListener()
        ctx.assignable().enterRule(assign_listener)
        # ctx.singleExpression().enterRule(expression_listener)  # FIXME No ExpressionListener yet
        self._var_decl = nodes.VariableDeclarator(
            loc, assign_listener.result, None
        )  # FIXME


class StatementListener(JSBaseListener):
    _stmt: nodes.Statement

    @property
    def statement(self) -> nodes.Statement:
        """Statement AST node generated after parse tree walking."""

        return self._stmt

    def enterStatement(self, ctx: JavaScriptParser.StatementContext):
        """Obtain an actual statement."""
        logging.debug("Entered section Statement")
        ctx.getChild(0).enterRule(self)

    def enterBlock(self, ctx: JavaScriptParser.BlockContext):
        """Listener for BlockStatement."""
        logging.debug("Entered section Block")

        stmt_list: List[nodes.Statement] = []
        for stmt in ctx.statementList().children:
            stmt_listener = StatementListener()
            stmt.enterRule(stmt_listener)
            stmt_list.append(stmt_listener.statement)

        loc = _get_source_location(ctx, None)  # FIXME source param is None
        self._stmt = nodes.BlockStatement(loc, stmt_list)

    def enterVariableStatement(self, ctx: JavaScriptParser.VariableStatementContext):
        logging.debug("Entered section VariableStatement")
        ctx.variableDeclarationList().enterRule(self)

    def enterVariableDeclarationList(
        self, ctx: JavaScriptParser.VariableDeclarationListContext
    ):
        """Listener for VariableDeclaration."""
        logging.debug("Entered section VariableDeclaration")

        var_modifier: nodes.VarDeclKind = ctx.varModifier().getText()
        var_decls: List[nodes.VariableDeclarator] = []

        for var_decl in ctx.variableDeclaration():
            var_decl_listener = VariableDeclarationListener()
            var_decl.enterRule(var_decl_listener)
            var_decls.append(var_decl_listener.var_declarator)

        loc = _get_source_location(ctx, None)
        self._stmt = nodes.VariableDeclaration(loc, var_modifier, var_decls)

    def enterEmptyStatement(self, ctx: JavaScriptParser.EmptyStatementContext):
        """Listener for EmptyStatement."""
        logging.debug("Entered section EmptyStatement")
        loc = _get_source_location(ctx, None)
        self._stmt = nodes.EmptyStatement(loc)
        pass

    def enterExpressionStatement(
        self, ctx: JavaScriptParser.ExpressionStatementContext
    ):
        """Listener for ExpressionStatement.
        TODO: check up expression containers.
        """
        logging.debug("Entered section ExpressionStatement")
        pass

    def enterIfStatement(self, ctx: JavaScriptParser.IfStatementContext):
        """Listener for IfStatement."""
        logging.debug("Entered section IfStatement")
        pass

    def enterFunctionDeclaration(
        self, ctx: JavaScriptParser.FunctionDeclarationContext
    ):
        """Listener for FunctionDeclaration."""
        logging.debug("Entered section FunctionDeclaration")
        pass

    # TODO: import/export, ClassDeclaration, iter statements, continue. break, return


class SourceElementListener(JSBaseListener):
    """The proxy between Program and Statement."""

    _elems: List[nodes.Statement] = []

    @property
    def source_elements(self) -> List[nodes.Statement]:
        """Source elements AST nodes generated after parse tree walking."""

        return self._elems

    def enterSourceElement(self, ctx: JavaScriptParser.SourceElementContext):
        logging.debug("Entered section Source Element")
        stmt_listener = StatementListener()
        stmt = ctx.statement()
        stmt.enterRule(stmt_listener)
        self._elems.append(stmt_listener.statement)


class ASTListener(JSBaseListener):
    """AST listener."""

    _program_node: Optional[nodes.Program] = None
    _source_type: nodes.SourceTypeLiteral

    @property
    def program_node(self) -> nodes.Program:
        """The `Program` AST node generated after parse tree walking."""
        if self._program_node is None:
            raise ValueError("Program AST node is None, did you run the listener?")

        return self._program_node

    def __init__(self, source_type: nodes.SourceTypeLiteral = "script"):
        """AST listener constructor.

        Args:
            source_type (nodes.SourceTypeLiteral): source type. Could be `script` or `module`. Set to
                `script` by default.
        """
        self._source_type = source_type

    def enterProgram(self, ctx: JavaScriptParser.ProgramContext):
        logging.debug("Entered section Program")
        logging.debug("JS source type: %s", self._source_type)

        hashbang = ctx.HashBangLine()
        if hashbang is not None:
            hashbang_exec = hashbang.getText()[2:]
            logging.debug('Found a hashbang "%s"', hashbang_exec)
            # TODO treat it somehow

        source_elem_listener = SourceElementListener()

        for elem in ctx.sourceElements().children:
            elem.enterRule(source_elem_listener)

        loc = _get_source_location(ctx, None)  # FIXME add source name
        self._program_node = nodes.Program(
            loc, self._source_type, source_elem_listener.source_elements
        )
