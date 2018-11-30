# Generated from main/mp/parser/MP.g4 by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .MPParser import MPParser
else:
    from MPParser import MPParser

# This class defines a complete generic visitor for a parse tree produced by MPParser.

class MPVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by MPParser#program.
    def visitProgram(self, ctx:MPParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#declar.
    def visitDeclar(self, ctx:MPParser.DeclarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#mptype.
    def visitMptype(self, ctx:MPParser.MptypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#comment.
    def visitComment(self, ctx:MPParser.CommentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#andThen.
    def visitAndThen(self, ctx:MPParser.AndThenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#orElse.
    def visitOrElse(self, ctx:MPParser.OrElseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#body.
    def visitBody(self, ctx:MPParser.BodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#boollit.
    def visitBoollit(self, ctx:MPParser.BoollitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#keyword.
    def visitKeyword(self, ctx:MPParser.KeywordContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#exp.
    def visitExp(self, ctx:MPParser.ExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#exp1.
    def visitExp1(self, ctx:MPParser.Exp1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#exp2.
    def visitExp2(self, ctx:MPParser.Exp2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#exp3.
    def visitExp3(self, ctx:MPParser.Exp3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#exp4.
    def visitExp4(self, ctx:MPParser.Exp4Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#exp5.
    def visitExp5(self, ctx:MPParser.Exp5Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#indexExpression.
    def visitIndexExpression(self, ctx:MPParser.IndexExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#varDeclar.
    def visitVarDeclar(self, ctx:MPParser.VarDeclarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#listVarDeclar.
    def visitListVarDeclar(self, ctx:MPParser.ListVarDeclarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#singleVarDeclar.
    def visitSingleVarDeclar(self, ctx:MPParser.SingleVarDeclarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#listVar.
    def visitListVar(self, ctx:MPParser.ListVarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#varType.
    def visitVarType(self, ctx:MPParser.VarTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#singleVarType.
    def visitSingleVarType(self, ctx:MPParser.SingleVarTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#arrayVarType.
    def visitArrayVarType(self, ctx:MPParser.ArrayVarTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#lower.
    def visitLower(self, ctx:MPParser.LowerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#upper.
    def visitUpper(self, ctx:MPParser.UpperContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#funcType.
    def visitFuncType(self, ctx:MPParser.FuncTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#singleFuncType.
    def visitSingleFuncType(self, ctx:MPParser.SingleFuncTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#funcDeclar.
    def visitFuncDeclar(self, ctx:MPParser.FuncDeclarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#listPara.
    def visitListPara(self, ctx:MPParser.ListParaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#paraDeclar.
    def visitParaDeclar(self, ctx:MPParser.ParaDeclarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#procDeclar.
    def visitProcDeclar(self, ctx:MPParser.ProcDeclarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#literal.
    def visitLiteral(self, ctx:MPParser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#assignStatement.
    def visitAssignStatement(self, ctx:MPParser.AssignStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#listVarToAssign.
    def visitListVarToAssign(self, ctx:MPParser.ListVarToAssignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#ifStatement.
    def visitIfStatement(self, ctx:MPParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#bodyStmt.
    def visitBodyStmt(self, ctx:MPParser.BodyStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#bodyStmt2.
    def visitBodyStmt2(self, ctx:MPParser.BodyStmt2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#whileStatement.
    def visitWhileStatement(self, ctx:MPParser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#forStatement.
    def visitForStatement(self, ctx:MPParser.ForStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#expr2.
    def visitExpr2(self, ctx:MPParser.Expr2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#breakStatement.
    def visitBreakStatement(self, ctx:MPParser.BreakStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#continueStatement.
    def visitContinueStatement(self, ctx:MPParser.ContinueStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#returnStatement.
    def visitReturnStatement(self, ctx:MPParser.ReturnStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#withStatement.
    def visitWithStatement(self, ctx:MPParser.WithStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#compoundStatement.
    def visitCompoundStatement(self, ctx:MPParser.CompoundStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#funcallExp.
    def visitFuncallExp(self, ctx:MPParser.FuncallExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#listExp.
    def visitListExp(self, ctx:MPParser.ListExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#callStatement.
    def visitCallStatement(self, ctx:MPParser.CallStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#statement.
    def visitStatement(self, ctx:MPParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#varElement.
    def visitVarElement(self, ctx:MPParser.VarElementContext):
        return self.visitChildren(ctx)



del MPParser