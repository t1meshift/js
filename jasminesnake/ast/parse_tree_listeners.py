"""Parse tree listeners.

Basically, you should use ASTListener(source_type: SourceTypeLiteral) in most cases.

Todo:
    * Fill `source` field in SourceLocation and pass it to each `_get_source_location()` call.
    * Compare `SourceLocation` creation behavior with the one in Acorn/ESPrima
"""

import logging
from typing import Optional, List, Union
import antlr4.ParserRuleContext
from antlr4 import ErrorNode, ParserRuleContext

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


class NodeListener(JSBaseListener):
    def visitErrorNode(self, node: ErrorNode):
        pass

    def enterEveryRule(self, ctx: ParserRuleContext):
        pass


class AssignmentOperatorListener(JSBaseListener):
    _op: nodes.AssignmentOperator

    @property
    def oper(self):
        return self._op

    def enterAssignmentOperator(self, ctx: JavaScriptParser.AssignmentOperatorContext):
        ops = nodes.AssignmentOperator
        ops_list = [
            (ctx.MultiplyAssign(), ops.MUL),
            (ctx.DivideAssign(), ops.DIV),
            (ctx.ModulusAssign(), ops.MOD),
            (ctx.PlusAssign(), ops.ADD),
            (ctx.MinusAssign(), ops.SUB),
            (ctx.LeftShiftArithmeticAssign(), ops.SHL),
            (ctx.RightShiftArithmeticAssign(), ops.SHR),
            (ctx.RightShiftLogicalAssign(), ops.SHR_LOGIC),
            (ctx.BitAndAssign(), ops.AND),
            (ctx.BitXorAssign(), ops.XOR),
            (ctx.BitOrAssign(), ops.OR),
            (ctx.PowerAssign(), ops.POW),
        ]

        for (op_cond, op) in ops_list:
            if op_cond is not None:
                self._op = op
                break


class LiteralListener(JSBaseListener):
    _literal: nodes.Literal

    @property
    def literal(self):
        return self._literal

    def enterLiteral(self, ctx: JavaScriptParser.LiteralContext):
        loc = _get_source_location(ctx, None)
        if ctx.NullLiteral() is not None:
            self._literal = nodes.NullLiteral(loc)
        elif ctx.BooleanLiteral() is not None:
            value = ctx.BooleanLiteral().getText() == "true"
            self._literal = nodes.BooleanLiteral(loc, value)
        elif ctx.StringLiteral() is not None:
            self._literal = nodes.StringLiteral(loc, ctx.StringLiteral().getText())
        else:
            ctx.getChild(0).enterRule(self)

    def enterNumericLiteral(self, ctx: JavaScriptParser.NumericLiteralContext):
        # Thank you, PEP-515, very cool!
        loc = _get_source_location(ctx, None)
        value = float(ctx.DecimalLiteral().getText())
        self._literal = nodes.NumericLiteral(loc, value)

    def enterBigintLiteral(self, ctx: JavaScriptParser.BigintLiteralContext):
        raise NotImplementedError("Bigint literals")


class ArrayLiteralExpandListener(JSBaseListener):
    _exprs: List[Union[nodes.Expression, nodes.SpreadElement]]

    @property
    def expressions(self):
        return self._exprs

    def enterArrayLiteral(self, ctx: JavaScriptParser.ArrayLiteralContext):
        logging.debug("Entered section ArrayLiteral")
        ctx.elementList().enterRule(self)

    def enterElementList(self, ctx: JavaScriptParser.ElementListContext):
        logging.debug("Entered section ElementList")
        self._exprs = []
        for expr in ctx.arrayElement():
            expr.enterRule(self)

    def enterArrayElement(self, ctx: JavaScriptParser.ArrayElementContext):
        logging.debug("Entered section ArrayElement")
        expr_listener = ExpressionListener()
        ctx.singleExpression().enterRule(expr_listener)
        if ctx.Ellipsis() is not None:
            loc = _get_source_location(ctx, None)
            self._exprs.append(nodes.SpreadElement(loc, expr_listener.expression))
        else:
            self._exprs.append(expr_listener.expression)


class ExpressionListener(JSBaseListener):
    _expr: nodes.Expression

    @property
    def expression(self):
        return self._expr

    def enterExpressionStatement(
        self, ctx: JavaScriptParser.ExpressionStatementContext
    ):
        ctx.expressionSequence().enterRule(self)
        raise NotImplementedError("ExpressionStatement")

    def enterExpressionSequence(self, ctx: JavaScriptParser.ExpressionSequenceContext):
        expressions: List[nodes.Expression] = []
        loc = _get_source_location(ctx, None)
        for expr in ctx.singleExpression():
            expr_listener = ExpressionListener()
            expr.enterRule(expr_listener)
            expressions.append(expr_listener.expression)
        self._expr = nodes.SequenceExpression(loc, expressions)

    def enterParenthesizedExpression(
        self, ctx: JavaScriptParser.ParenthesizedExpressionContext
    ):
        ctx.expressionSequence().enterRule(self)
        raise NotImplementedError("ParenthesizedExpression")

    def enterLiteralExpression(self, ctx: JavaScriptParser.LiteralExpressionContext):
        literal_listener = LiteralListener()
        ctx.literal().enterRule(literal_listener)
        self._expr = literal_listener.literal

    def enterFunctionExpression(self, ctx: JavaScriptParser.FunctionExpressionContext):
        logging.debug("Entered section FunctionExpression")
        raise NotImplementedError("FunctionExpression")  # TODO

    def enterClassExpression(self, ctx: JavaScriptParser.ClassExpressionContext):
        logging.debug("Entered section ClassExpression")
        raise NotImplementedError("ClassExpression")  # TODO

    def enterMemberIndexExpression(
        self, ctx: JavaScriptParser.MemberIndexExpressionContext
    ):
        logging.debug("Entered section MemberIndexExpression")
        raise NotImplementedError("MemberIndexExpression")  # TODO

    def enterMemberDotExpression(
        self, ctx: JavaScriptParser.MemberDotExpressionContext
    ):
        logging.debug("Entered section MemberDotExpression")
        raise NotImplementedError("MemberDotExpression")  # TODO

    def enterArgumentsExpression(
        self, ctx: JavaScriptParser.ArgumentsExpressionContext
    ):
        logging.debug("Entered section ArgumentsExpression")
        raise NotImplementedError("ArgumentsExpression")  # TODO

    def enterNewExpression(self, ctx: JavaScriptParser.NewExpressionContext):
        logging.debug("Entered section NewExpression")
        raise NotImplementedError("NewExpression")  # TODO

    def enterMetaExpression(self, ctx: JavaScriptParser.MetaExpressionContext):
        logging.debug("Entered section MetaExpression")
        raise NotImplementedError("MetaExpression")  # TODO

    def enterPostIncrementExpression(
        self, ctx: JavaScriptParser.PostIncrementExpressionContext
    ):
        logging.debug("Entered section PostIncrementExpression")
        raise NotImplementedError("PostIncrementExpression")  # TODO

    def enterPostDecreaseExpression(
        self, ctx: JavaScriptParser.PostDecreaseExpressionContext
    ):
        logging.debug("Entered section PostDecreaseExpression")
        raise NotImplementedError("PostDecreaseExpression")  # TODO

    def enterDeleteExpression(self, ctx: JavaScriptParser.DeleteExpressionContext):
        logging.debug("Entered section DeleteExpression")
        raise NotImplementedError("DeleteExpression")  # TODO

    def enterVoidExpression(self, ctx: JavaScriptParser.VoidExpressionContext):
        logging.debug("Entered section VoidExpression")
        raise NotImplementedError("VoidExpression")  # TODO

    def enterTypeofExpression(self, ctx: JavaScriptParser.TypeofExpressionContext):
        logging.debug("Entered section TypeofExpression")
        raise NotImplementedError("TypeofExpression")  # TODO

    def enterPreIncrementExpression(
        self, ctx: JavaScriptParser.PreIncrementExpressionContext
    ):
        logging.debug("Entered section PreIncrementExpression")
        raise NotImplementedError("PreIncrementExpression")  # TODO

    def enterPreDecreaseExpression(
        self, ctx: JavaScriptParser.PreDecreaseExpressionContext
    ):
        logging.debug("Entered section PreDecreaseExpression")
        raise NotImplementedError("PreDecreaseExpression")  # TODO

    def enterUnaryPlusExpression(
        self, ctx: JavaScriptParser.UnaryPlusExpressionContext
    ):
        logging.debug("Entered section UnaryPlusExpression")
        raise NotImplementedError("UnaryPlusExpression")  # TODO

    def enterUnaryMinusExpression(
        self, ctx: JavaScriptParser.UnaryMinusExpressionContext
    ):
        logging.debug("Entered section UnaryMinusExpression")
        raise NotImplementedError("UnaryMinusExpression")  # TODO

    def enterBitNotExpression(self, ctx: JavaScriptParser.BitNotExpressionContext):
        logging.debug("Entered section BitNotExpression")
        raise NotImplementedError("BitNotExpression")  # TODO

    def enterNotExpression(self, ctx: JavaScriptParser.NotExpressionContext):
        logging.debug("Entered section NotExpression")
        raise NotImplementedError("NotExpression")  # TODO

    def enterPowerExpression(self, ctx: JavaScriptParser.PowerExpressionContext):
        logging.debug("Entered section PowerExpression")
        raise NotImplementedError("PowerExpression")  # TODO

    def enterMultiplicativeExpression(
        self, ctx: JavaScriptParser.MultiplicativeExpressionContext
    ):
        logging.debug("Entered section MultiplicativeExpression")
        raise NotImplementedError("MultiplicativeExpression")  # TODO

    def enterAdditiveExpression(self, ctx: JavaScriptParser.AdditiveExpressionContext):
        logging.debug("Entered section AdditiveExpression")
        raise NotImplementedError("AdditiveExpression")  # TODO

    def enterCoalesceExpression(self, ctx: JavaScriptParser.CoalesceExpressionContext):
        logging.debug("Entered section MemberIndexExpression")
        raise NotImplementedError("MemberIndexExpression")  # TODO

    def enterBitShiftExpression(self, ctx: JavaScriptParser.BitShiftExpressionContext):
        logging.debug("Entered section BitShiftExpression")
        raise NotImplementedError("BitShiftExpression")  # TODO

    def enterRelationalExpression(
        self, ctx: JavaScriptParser.RelationalExpressionContext
    ):
        logging.debug("Entered section RelationalExpression")
        raise NotImplementedError("RelationalExpression")  # TODO

    def enterInExpression(self, ctx: JavaScriptParser.InExpressionContext):
        logging.debug("Entered section InExpression")
        raise NotImplementedError("InExpression")  # TODO

    def enterEqualityExpression(self, ctx: JavaScriptParser.EqualityExpressionContext):
        logging.debug("Entered section EqualityExpression")
        raise NotImplementedError("EqualityExpression")  # TODO

    def enterBitAndExpression(self, ctx: JavaScriptParser.BitAndExpressionContext):
        logging.debug("Entered section BitAndExpression")
        raise NotImplementedError("BitAndExpression")  # TODO

    def enterBitOrExpression(self, ctx: JavaScriptParser.BitOrExpressionContext):
        logging.debug("Entered section BitOrExpression")
        raise NotImplementedError("BitOrExpression")  # TODO

    def enterBitXOrExpression(self, ctx: JavaScriptParser.BitXOrExpressionContext):
        logging.debug("Entered section BitXOrExpression")
        raise NotImplementedError("BitXOrExpression")  # TODO

    def enterLogicalAndExpression(
        self, ctx: JavaScriptParser.LogicalAndExpressionContext
    ):
        logging.debug("Entered section LogicalAndExpression")
        raise NotImplementedError("LogicalAndExpression")  # TODO

    def enterLogicalOrExpression(
        self, ctx: JavaScriptParser.LogicalOrExpressionContext
    ):
        logging.debug("Entered section LogicalOrExpression")
        raise NotImplementedError("LogicalOrExpression")  # TODO

    def enterTernaryExpression(self, ctx: JavaScriptParser.TernaryExpressionContext):
        logging.debug("Entered section TernaryExpression")
        raise NotImplementedError("TernaryExpression")  # TODO

    def enterAssignmentExpression(
        self, ctx: JavaScriptParser.AssignmentExpressionContext
    ):
        logging.debug("Entered section AssignmentExpression")
        left_lst = ExpressionListener()
        right_lst = ExpressionListener()
        ctx.singleExpression(0).enterRule(left_lst)
        ctx.singleExpression(1).enterRule(right_lst)

        loc = _get_source_location(ctx, None)
        left = left_lst.expression
        right = right_lst.expression
        self._expr = nodes.AssignmentExpression(
            loc, nodes.AssignmentOperator.ASSIGN, left, right
        )

    def enterAssignmentOperatorExpression(
        self, ctx: JavaScriptParser.AssignmentOperatorExpressionContext
    ):
        logging.debug("Entered section AssignmentOperatorExpression")
        left_lst = ExpressionListener()
        right_lst = ExpressionListener()
        op_lst = AssignmentOperatorListener()
        ctx.singleExpression(0).enterRule(left_lst)
        ctx.singleExpression(1).enterRule(right_lst)
        ctx.assignmentOperator().enterRule(op_lst)

        loc = _get_source_location(ctx, None)
        left = left_lst.expression
        right = right_lst.expression
        op = op_lst.oper
        self._expr = nodes.AssignmentExpression(loc, op, left, right)

    def enterImportExpression(self, ctx: JavaScriptParser.ImportExpressionContext):
        logging.debug("Entered section ImportExpression")
        raise NotImplementedError("ImportExpression")  # TODO

    def enterThisExpression(self, ctx: JavaScriptParser.ThisExpressionContext):
        logging.debug("Entered section ThisExpression")
        loc = _get_source_location(ctx, None)
        self._expr = nodes.ThisExpression(loc)

    def enterIdentifierExpression(
        self, ctx: JavaScriptParser.IdentifierExpressionContext
    ):
        logging.debug("Entered section IdentifierExpression")
        ctx.identifier().enterRule(self)

    def enterIdentifier(self, ctx: JavaScriptParser.IdentifierContext):
        logging.debug("Entered section Identifier")
        loc = _get_source_location(ctx, None)
        self._expr = nodes.Identifier(loc, ctx.getText())

    def enterSuperExpression(self, ctx: JavaScriptParser.SuperExpressionContext):
        logging.debug("Entered section SuperExpression")
        loc = _get_source_location(ctx, None)
        self._expr = nodes.Super(loc)

    def enterArrayLiteralExpression(
        self, ctx: JavaScriptParser.ArrayLiteralExpressionContext
    ):
        logging.debug("Entered section ArrayLiteralExpression")
        arr_expand_lst = ArrayLiteralExpandListener()
        ctx.arrayLiteral().enterRule(arr_expand_lst)
        loc = _get_source_location(ctx, None)
        self._expr = nodes.ArrayExpression(loc, arr_expand_lst.expressions)

    def enterObjectLiteralExpression(
        self, ctx: JavaScriptParser.ObjectLiteralExpressionContext
    ):
        logging.debug("Entered section ObjectLiteralExpression")
        raise NotImplementedError("ObjectLiteralExpression")  # TODO


class AssignableListener(NodeListener):
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
        loc = _get_source_location(ctx, None)

        elems = []
        if ctx.elementList() is not None:
            arr_exp_lst = ArrayLiteralExpandListener()
            ctx.elementList().enterRule(arr_exp_lst)
            elems += arr_exp_lst.expressions

        self._result = nodes.ArrayPattern(loc, elems)

    def enterObjectLiteral(self, ctx: JavaScriptParser.ObjectLiteralContext):
        logging.debug("Entered section ObjectLiteral")
        raise NotImplementedError("ObjectLiteral assignment")  # TODO


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

        init = None  # or value from ExpressionListener
        if ctx.singleExpression() is not None:
            expression_listener = ExpressionListener()
            ctx.singleExpression().enterRule(expression_listener)
            init = expression_listener.expression

        self._var_decl = nodes.VariableDeclarator(loc, assign_listener.result, init)


class StatementListener(JSBaseListener):
    _stmt: nodes.Statement

    @property
    def statement(self) -> nodes.Statement:
        """Statement AST node generated after parse tree walking."""

        return self._stmt

    def __init__(self, in_loop: bool = False, in_func: bool = False):
        """
        Statement listener. Generates a Statement.

        Args:
            in_loop (bool): allow `continue` and `break` statements
            in_func (bool): allow `return` statement
        """
        self._in_loop = in_loop
        self._in_func = in_func

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

        loc = _get_source_location(ctx, None)
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
        """Listener for ExpressionStatement."""
        logging.debug("Entered section ExpressionStatement")
        expr_listener = ExpressionListener()
        ctx.expressionSequence().enterRule(expr_listener)
        loc = _get_source_location(ctx, None)
        self._stmt = nodes.ExpressionStatement(loc, expr_listener.expression)

    def enterIfStatement(self, ctx: JavaScriptParser.IfStatementContext):
        """Listener for IfStatement."""
        logging.debug("Entered section IfStatement")
        raise NotImplementedError("IfStatement")

    def enterFunctionDeclaration(
        self, ctx: JavaScriptParser.FunctionDeclarationContext
    ):
        """Listener for FunctionDeclaration."""
        logging.debug("Entered section FunctionDeclaration")
        raise NotImplementedError("FunctionDeclaration")

    def enterDoStatement(self, ctx: JavaScriptParser.DoStatementContext):
        """Listener for DoStatement (do-while)."""
        raise NotImplementedError("DoWhileStatement")

    def enterWhileStatement(self, ctx: JavaScriptParser.WhileStatementContext):
        """Listener for WhileStatement."""
        logging.debug("Entered section WhileStatement")
        raise NotImplementedError("WhileStatement")

    def enterForStatement(self, ctx: JavaScriptParser.ForStatementContext):
        """Listener for ForStatement."""
        logging.debug("Entered section ForStatement")
        raise NotImplementedError("ForStatement")

    def enterForInStatement(self, ctx: JavaScriptParser.ForInStatementContext):
        """Listener for ForInStatement."""
        logging.debug("Entered section ForInStatement")
        raise NotImplementedError("ForInStatement")

    def enterContinueStatement(self, ctx: JavaScriptParser.ContinueStatementContext):
        logging.debug("Entered section ContinueStatement")
        raise NotImplementedError("ContinueStatement")

    def enterBreakStatement(self, ctx: JavaScriptParser.BreakStatementContext):
        logging.debug("Entered BreakStatement")
        raise NotImplementedError("BreakStatement")

    def enterReturnStatement(self, ctx: JavaScriptParser.ReturnStatementContext):
        logging.debug("Entered ReturnStatement")
        raise NotImplementedError("ReturnStatement")

    def enterImportStatement(self, ctx: JavaScriptParser.ImportStatementContext):
        logging.debug("Entered ImportStatement")
        raise NotImplementedError("ImportStatement")

    def enterExportDeclaration(self, ctx: JavaScriptParser.ExportDeclarationContext):
        logging.debug("Entered ExportDeclaration")
        raise NotImplementedError("ExportDeclaration")

    def enterExportDefaultDeclaration(
        self, ctx: JavaScriptParser.ExportDefaultDeclarationContext
    ):
        logging.debug("Entered ExportDefaultDeclaration")
        raise NotImplementedError("ExportDefaultDeclaration")

    def enterClassDeclaration(self, ctx: JavaScriptParser.ClassDeclarationContext):
        logging.debug("Entered ClassDeclaration")
        raise NotImplementedError("ClassDeclaration")


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
