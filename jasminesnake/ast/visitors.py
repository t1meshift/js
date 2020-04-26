from lex import JavaScriptParserVisitor, JavaScriptParser
import ast.nodes

JSBaseVisitor = JavaScriptParserVisitor.JavaScriptParserVisitor
JSParser = JavaScriptParser.JavaScriptParser


class JSASTVisitor(JSBaseVisitor):
    def visitVariableDeclarationList(
        self, ctx: JSParser.VariableDeclarationListContext
    ):
        pass
