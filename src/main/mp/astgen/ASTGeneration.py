#1612537
#To generate test suggestion, remove it if you like
import sys
import os

sys.path.append(os.path.abspath('./../../../../target/main/mp/parser/'))
from MPVisitor import MPVisitor
from MPParser import MPParser

sys.path.append(os.path.abspath('./../utils/'))
from AST import *
from functools import *


class ASTGeneration(MPVisitor):
    def visitProgram(self, ctx: MPParser.ProgramContext):
        return Program(reduce(lambda x, y: x + self.visit(y), ctx.declar(), []))

    def visitDeclar(self, ctx: MPParser.DeclarContext):
        if ctx.varDeclar():
            return self.visit(ctx.varDeclar())
        if ctx.funcDeclar():
            return self.visit(ctx.funcDeclar())
        else:
            return self.visit(ctx.procDeclar())

    #VAR DECLARATION
    def visitVarDeclar(self, ctx: MPParser.VarDeclarContext):
        return self.visit(ctx.listVarDeclar())

    def visitListVarDeclar(self, ctx: MPParser.ListVarDeclarContext):
        if ctx.listVarDeclar():
            return self.visit(ctx.singleVarDeclar()) + self.visit(ctx.listVarDeclar())
        else:
            return self.visit(ctx.singleVarDeclar())

    def visitSingleVarDeclar(self, ctx: MPParser.SingleVarDeclarContext):
        # if map(lambda x: VarDecl(self.visit()),self.visit(ctx.listVar()))
        result = []
        listVar = self.visit(ctx.listVar())
        for x in listVar:
            result += [VarDecl(x, self.visit(ctx.varType()))]
        return result
        #return list(map(lambda x: VarDecl(x, self.visit(ctx.varType())), listVar))

    def visitListVar(self, ctx: MPParser.ListVarContext):
        if ctx.listVar():
            return [Id(ctx.ID().getText())] + self.visit(ctx.listVar())
        else:
            return [Id(ctx.ID().getText())]

    def visitVarType(self, ctx: MPParser.VarTypeContext):
        if ctx.singleVarType():
            return self.visit(ctx.singleVarType())
        else:
            return self.visit(ctx.arrayVarType())

    def visitSingleVarType(self, ctx: MPParser.SingleVarTypeContext):
        if ctx.INTTYPE():
            return IntType()
        if ctx.REALTYPE():
            return FloatType()
        if ctx.BOOLTYPE():
            return BoolType()
        if ctx.STRINGTYPE():
            return StringType()

    def visitArrayVarType(self, ctx: MPParser.ArrayVarTypeContext):
        return ArrayType(ctx.lower().getText(), ctx.upper().getText(), self.visit(ctx.singleVarType()))

    # FUNCTION DECLARATION
    def visitSingleFuncType(self, ctx: MPParser.SingleFuncTypeContext):
        return self.visit(ctx.singleVarType()) if ctx.singleVarType() else []

    def visitFuncDeclar(self, ctx: MPParser.FuncDeclarContext):
        return [FuncDecl(
            Id(ctx.ID().getText()),
            self.visit(ctx.listPara()) if ctx.listPara() else [],
            self.visit(ctx.varDeclar()) if ctx.varDeclar() else [],
            self.visit(ctx.compoundStatement()
                       ) if ctx.compoundStatement() else [],
            self.visit(ctx.varType())
        )]

    def visitListPara(self, ctx: MPParser.ListParaContext):
        return (self.visit(ctx.paraDeclar()) + self.visit(ctx.listPara())) if ctx.listPara() else self.visit(ctx.paraDeclar())

    def visitParaDeclar(self, ctx: MPParser.ParaDeclarContext):
        return list(map(lambda x: VarDecl(x, self.visit(ctx.varType())), self.visit(ctx.listVar())))

    # PROCEDURE DECLARATION
    def visitProcDeclar(self, ctx: MPParser.ProcDeclarContext):
        return [FuncDecl(
            Id(ctx.ID().getText()),
            self.visit(ctx.listPara()) if ctx.listPara() else [],
            self.visit(ctx.varDeclar()) if ctx.varDeclar() else [],
            self.visit(ctx.compoundStatement()
                       ) if ctx.compoundStatement() else []
        )]

    #EXPRESSION
    def visitExp(self, ctx: MPParser.ExpContext):
        if ctx.exp():
            if ctx.andThen():
                return BinaryOp("andthen", self.visit(ctx.exp()), self.visit(ctx.exp1()))
                #[self.visit(ctx.exp()) + self.visit(ctx.andThen()) + self.visit(ctx.exp1())]
            else:
                return BinaryOp("orelse", self.visit(ctx.exp()), self.visit(ctx.exp1()))
        else:
            return self.visit(ctx.exp1())

    def visitExp1(self, ctx: MPParser.Exp1Context):
        if ctx.getChildCount() == 3:
            if ctx.EQUAL():
                return BinaryOp(ctx.EQUAL().getText(), self.visit(ctx.exp2(0)), self.visit(ctx.exp2(1)))
            elif ctx.NOTEQUAL():
                return BinaryOp(ctx.NOTEQUAL().getText(), self.visit(ctx.exp2(0)), self.visit(ctx.exp2(1)))
            elif ctx.LESS():
                return BinaryOp(ctx.LESS().getText(), self.visit(ctx.exp2(0)), self.visit(ctx.exp2(1)))
            elif ctx.LESSEQUAL():
                return BinaryOp(ctx.LESSEQUAL().getText(), self.visit(ctx.exp2(0)), self.visit(ctx.exp2(1)))
            elif ctx.GREATER():
                return BinaryOp(ctx.GREATER().getText(), self.visit(ctx.exp2(0)), self.visit(ctx.exp2(1)))
            elif ctx.GREATEREQUAL():
                return BinaryOp(ctx.GREATEREQUAL().getText(), self.visit(ctx.exp2(0)), self.visit(ctx.exp2(1)))
        else:
            return self.visit(ctx.exp2(0))

    def visitExp2(self, ctx: MPParser.Exp2Context):
        if ctx.exp2():
            if ctx.ADD():
                return BinaryOp(ctx.ADD().getText(), self.visit(ctx.exp2()), self.visit(ctx.exp3()))
            elif ctx.SUB():
                return BinaryOp(ctx.SUB().getText(), self.visit(ctx.exp2()), self.visit(ctx.exp3()))
            elif ctx.OR():
                return BinaryOp(ctx.OR().getText(), self.visit(ctx.exp2()), self.visit(ctx.exp3()))
        else:
            return self.visit(ctx.exp3())

    def visitExp3(self, ctx: MPParser.Exp3Context):
        if ctx.exp3():
            if ctx.DIVISION():
                return BinaryOp(ctx.DIVISION().getText(), self.visit(ctx.exp3()), self.visit(ctx.exp4()))
            elif ctx.MUL():
                return BinaryOp(ctx.MUL().getText(), self.visit(ctx.exp3()), self.visit(ctx.exp4()))
            elif ctx.DIV():
                return BinaryOp(ctx.DIV().getText(), self.visit(ctx.exp3()), self.visit(ctx.exp4()))
            elif ctx.AND():
                return BinaryOp(ctx.AND().getText(), self.visit(ctx.exp3()), self.visit(ctx.exp4()))
            elif ctx.MOD():
                return BinaryOp(ctx.MOD().getText(), self.visit(ctx.exp3()), self.visit(ctx.exp4()))
            else:
                return BinaryOp("Unknown", self.visit(ctx.exp3()), self.visit(ctx.exp4()))
        else:
            return self.visit(ctx.exp4())

    def visitExp4(self, ctx: MPParser.Exp4Context):
        if (ctx.SUB() or ctx.NOT()):
            if ctx.SUB():
                return UnaryOp(ctx.SUB().getText(), self.visit(ctx.exp4()))
            elif ctx.NOT():
                return UnaryOp(ctx.NOT().getText(), self.visit(ctx.exp4()))
        else:
            return self.visit(ctx.exp5())

    def visitExp5(self, ctx: MPParser.Exp5Context):
        if ctx.literal():
            return self.visit(ctx.literal())
        elif ctx.ID():
            return Id(ctx.ID().getText())
        elif ctx.funcallExp():
            return self.visit(ctx.funcallExp())
        elif ctx.indexExpression():
            return self.visit(ctx.indexExpression())  # self.visit(ctx.indexExpression())
        elif ctx.LB() and ctx.RB():
            return self.visit(ctx.exp())

    def visitLiteral(self, ctx: MPParser.LiteralContext):
        if ctx.INTLIT():
            return IntLiteral(int(ctx.INTLIT().getText()))
        elif ctx.FLOATLIT():
            return FloatLiteral(float(ctx.FLOATLIT().getText()))
        elif ctx.STRINGLIT():
            return StringLiteral(str(ctx.STRINGLIT().getText()))
        elif ctx.boollit():
            return BooleanLiteral(self.visit(ctx.boollit()))
        else:
            return "UnknownType"
    
    def visitBoollit(self, ctx:MPParser.BoollitContext):
        if (ctx.TRUE()):
            return True
        else:
            return False

    def visitIndexExpression(self, ctx:MPParser.IndexExpressionContext):
        return ArrayCell(Id(ctx.ID().getText()) if ctx.ID() else self.visit(ctx.funcallExp()) if ctx.funcallExp() else "Unknown", self.visit(ctx.exp()))

    # STATEMENT
    ## ASSIGN STATEMENT
    def visitAssignStatement(self, ctx: MPParser.AssignStatementContext):
        #return list(map(lambda x: Assign(x, self.visit(ctx.exp())), self.visit(ctx.listVarToAssign())))
        newList = self.visit(ctx.listVarToAssign()) + [self.visit(ctx.exp())]
        i = len(newList) - 1
        result = []
        while i > 0:
            result += [Assign(newList[i-1], newList[i])]
            i -= 1
        return result

    def visitListVarToAssign(self, ctx: MPParser.ListVarToAssignContext):
        return ([self.visit(ctx.varElement())] + self.visit(ctx.listVarToAssign())) if ctx.listVarToAssign() else [self.visit(ctx.varElement())]

    def visitVarElement(self, ctx: MPParser.VarElementContext):
        if ctx.ID():
            return Id(ctx.ID().getText())
        elif ctx.indexExpression():
            return self.visit(ctx.indexExpression())  # Not define
        else:
            return "Unknown"

    ## IF STATEMENT
    def visitIfStatement(self, ctx: MPParser.IfStatementContext):
        if (not ctx.ELSE()):  # if no else
            return [If(self.visit(ctx.exp()), self.visit(ctx.bodyStmt()))]
        else:  # if else
            return [If(self.visit(ctx.exp()), self.visit(ctx.bodyStmt()), self.visit(ctx.bodyStmt2()))]

    # WHILE STATEMENT
    def visitWhileStatement(self, ctx: MPParser.WhileStatementContext):
        return [While(self.visit(ctx.exp()), self.visit(ctx.bodyStmt()))]

    # FOR STATEMENT
    def visitForStatement(self, ctx: MPParser.ForStatementContext):
        return [For(Id(ctx.ID().getText()), self.visit(ctx.exp()), self.visit(ctx.expr2()), True if ctx.TO() else False, self.visit(ctx.bodyStmt()))]

    def visitExpr2(self, ctx: MPParser.Expr2Context):
        return self.visit(ctx.exp())

    # BREAK STATEMENT
    def visitBreakStatement(self, ctx: MPParser.BreakStatementContext):
        return [Break()]
    # CONTINUE STATEMENT

    def visitContinueStatement(self, ctx: MPParser.ContinueStatementContext):
        return [Continue()]
    # RETURN STATEMENT

    def visitReturnStatement(self, ctx: MPParser.ReturnStatementContext):
        return [Return(self.visit(ctx.exp()) if ctx.exp() else None)]

    # WITH STATEMENT

    def visitWithStatement(self, ctx: MPParser.WithStatementContext):
        return [With(self.visit(ctx.listVarDeclar()), self.visit(ctx.bodyStmt()))]
    # CALL STATEMENT

    def visitFuncallExp(self, ctx: MPParser.FuncallExpContext):
        if ctx.ID():
            return CallExpr(Id(ctx.ID().getText()), self.visit(ctx.listExp()) if ctx.listExp() else [])
        else:
            return CallExpr("Unknown", [])
    
    def visitCallStatement(self, ctx:MPParser.CallStatementContext):
        if ctx.ID():
            return [CallStmt(Id(ctx.ID().getText()), self.visit(ctx.listExp()) if ctx.listExp() else [])]
        else:
            return [CallStmt("Unknown", [])]
    
    def visitListExp(self, ctx: MPParser.ListExpContext):
        if ctx.listExp():
            return [self.visit(ctx.exp())] + self.visit(ctx.listExp())
        else:
            return [self.visit(ctx.exp())]

    def visitBodyStmt(self, ctx: MPParser.BodyStmtContext):
        if ctx.statement():
            return self.visit(ctx.statement())
        else:
            return self.visit(ctx.compoundStatement())

    def visitBodyStmt2(self, ctx: MPParser.BodyStmt2Context):
        return self.visit(ctx.bodyStmt())

    def visitStatement(self, ctx: MPParser.StatementContext):
        if ctx.assignStatement():
            return self.visit(ctx.assignStatement())
        elif ctx.ifStatement():
            return self.visit(ctx.ifStatement())
        elif ctx.whileStatement():
            return self.visit(ctx.whileStatement())
        elif ctx.forStatement():
            return self.visit(ctx.forStatement())
        elif ctx.withStatement():
            return self.visit(ctx.withStatement())
        elif ctx.callStatement():
            return self.visit(ctx.callStatement())
        elif ctx.breakStatement():
            return self.visit(ctx.breakStatement())
        elif ctx.continueStatement():
            return self.visit(ctx.continueStatement())
        elif ctx.returnStatement():
            return self.visit(ctx.returnStatement())
        else:
            return ["Unknown Statement"]

    def visitCompoundStatement(self, ctx: MPParser.CompoundStatementContext):
        result = []
        for x in ctx.statement():
            result += self.visit(x)
        return result

    # It's feel bad but true
    # def visitBuiltInExp(self, ctx:MPParser.BuiltInExpContext):
    #     if ctx.getIntExp():
    #         return self.visit(ctx.getIntExp())
    #     elif ctx.putIntExp():
    #         return self.visit(ctx.putIntExp())
    #     elif ctx.getFloatExp():
    #         return self.visit(ctx.getFloatExp())
    #     elif ctx.putFloatExp():
    #         return self.visit(ctx.putFloatExp())
    #     elif ctx.putFloatLnExp():
    #         return self.visit(ctx.putFloatLnExp())
    #     elif ctx.putIntLNExp():
    #         return self.visit(ctx.putIntLNExp())
    #     elif ctx.putBoolExp():
    #         return self.visit(ctx.putBoolExp())
    #     elif ctx.putBoolLNExp():
    #         return self.visit(ctx.putBoolLNExp())
    #     elif ctx.putStringExp():
    #         return self.visit(ctx.putStringExp())
    #     elif ctx.putStringLNExp():
    #         return self.visit(ctx.putStringLNExp())
    #     elif ctx.putLnExp():
    #         return self.visit(ctx.putLnExp())
    #     else:
    #         CallExpr("Unknown", [])
    
    # def visitBuiltInFunCall(self, ctx:MPParser.BuiltInFunCallContext):
    #     if ctx.getInt():
    #         return self.visit(ctx.getInt())
    #     elif ctx.putInt():
    #         return self.visit(ctx.putInt())
    #     elif ctx.getFloat():
    #         return self.visit(ctx.getFloat())
    #     elif ctx.putFloat():
    #         return self.visit(ctx.putFloat())
    #     elif ctx.putFloatLn():
    #         return self.visit(ctx.putFloatLn())
    #     elif ctx.putIntLN():
    #         return self.visit(ctx.putIntLN())
    #     elif ctx.putBool():
    #         return self.visit(ctx.putBool())
    #     elif ctx.putBoolLN():
    #         return self.visit(ctx.putBoolLN())
    #     elif ctx.putString():
    #         return self.visit(ctx.putString())
    #     elif ctx.putStringLN():
    #         return self.visit(ctx.putStringLN())
    #     elif ctx.putLn():
    #         return self.visit(ctx.putLn())
    #     else:
    #         return CallStmt("Unknown",[])

    # def visitGetIntExp(self, ctx:MPParser.GetIntExpContext):
    #     return CallExpr(ctx.GETINT().getText(), [])
    # def visitPutIntExp(self, ctx:MPParser.PutIntExpContext):
    #     return CallExpr(ctx.PUTINT().getText(),self.visit(ctx.varElement()))
    # def visitPutIntLNExp(self, ctx:MPParser.PutIntLnExpContext):
    #     return CallExpr(ctx.PUTINTLN().getText(),self.visit(ctx.varElement()))
    # def visitGetFloatExp(self, ctx:MPParser.GetFloatExpContext):
    #     return CallExpr(ctx.GETFLOAT().getText(), [])
    # def visitPutFloatExp(self, ctx:MPParser.PutFloatLnExpContext):
    #     return CallExpr(ctx.PUTFLOAT().getText(), self.visit(ctx.varElement()))
    # def visitPutFloatLnExp(self, ctx:MPParser.PutFloatLnExpContext):
    #     return CallExpr(ctx.PUTFLOATLN().getText(), self.visit(ctx.varElement()))
    # def visitPutBoolExp(self, ctx:MPParser.PutBoolExpContext):
    #     return CallExpr(ctx.PUTBOOL().getText(), self.visit(ctx.varElement()))
    # def visitPutBoolLnExp(self, ctx:MPParser.PutBoolLnExpContext):
    #     return CallExpr(ctx.PUTBOOLLN().getText(), self.visit(ctx.varElement()))
    # def visitPutStringExp(self, ctx:MPParser.PutStringExpContext):
    #     return CallExpr(ctx.PUTSTRING().getText(), self.visit(ctx.varElement()))
    # def visitPutStringLnExp(self, ctx:MPParser.PutStringLnExpContext):
    #     return CallExpr(ctx.PUTSTRINGLN().getText(), self.visit(ctx.varElement()))
    # def visitPutLnExp(self, ctx:MPParser.PutLnExpContext):
    #     return CallExpr(ctx.PUTLN().getText(), [])
    
    # def visitGetInt(self, ctx:MPParser.GetIntContext):
    #     return CallStmt(ctx.GETINT().getText(), [])
    # def visitPutInt(self, ctx:MPParser.PutIntContext):
    #     return CallStmt(ctx.PUTINT().getText(),self.visit(ctx.varElement()))
    # def visitPutIntLN(self, ctx:MPParser.PutIntLnContext):
    #     return CallStmt(ctx.PUTINTLN().getText(),self.visit(ctx.varElement()))
    # def visitGetFloat(self, ctx:MPParser.GetFloatContext):
    #     return CallStmt(ctx.GETFLOAT().getText(), [])
    # def visitPutFloat(self, ctx:MPParser.PutFloatLnContext):
    #     return CallStmt(ctx.PUTFLOAT().getText(), self.visit(ctx.varElement()))
    # def visitPutFloatLn(self, ctx:MPParser.PutFloatLnContext):
    #     return CallStmt(ctx.PUTFLOATLN().getText(), self.visit(ctx.varElement()))
    # def visitPutBool(self, ctx:MPParser.PutBoolContext):
    #     return CallStmt(ctx.PUTBOOL().getText(), self.visit(ctx.varElement()))
    # def visitPutBoolLn(self, ctx:MPParser.PutBoolLnContext):
    #     return CallStmt(ctx.PUTBOOLLN().getText(), self.visit(ctx.varElement()))
    # def visitPutString(self, ctx:MPParser.PutStringContext):
    #     return CallStmt(ctx.PUTSTRING().getText(), self.visit(ctx.varElement()))
    # def visitPutStringLn(self, ctx:MPParser.PutStringLnContext):
    #     return CallStmt(ctx.PUTSTRINGLN().getText(), self.visit(ctx.varElement()))
    # def visitPutLn(self, ctx:MPParser.PutLnContext):
    #     return CallStmt(ctx.PUTLN().getText(), [])
    # def visitProgram(self,ctx:MPParser.ProgramContext):
    #     return Program([self.visit(x) for x in ctx.decl()])

    # def visitFuncdecl(self,ctx:MPParser.FuncdeclContext):
    #     local,cpstmt = self.visit(ctx.body())
    #     return FuncDecl(Id(ctx.ID().getText()),
    #                     [],
    #                     local,
    #                     cpstmt,
    #                     self.visit(ctx.mtype()))

    # def visitProcdecl(self,ctx:MPParser.ProcdeclContext):
    #     local,cpstmt = self.visit(ctx.body())
    #     return FuncDecl(Id(ctx.ID().getText()),
    #                     [],
    #                     local,
    #                     cpstmt)

    # def visitBody(self,ctx:MPParser.BodyContext):
    #     return [],[self.visit(ctx.stmt())] if ctx.stmt() else []

    # def visitStmt(self,ctx:MPParser.StmtContext):
    #     return self.visit(ctx.funcall())

    # def visitFuncall(self,ctx:MPParser.FuncallContext):
    #     return CallStmt(Id(ctx.ID().getText()),[self.visit(ctx.exp())] if ctx.exp() else [])

    # def visitExp(self,ctx:MPParser.ExpContext):
    #     return IntLiteral(int(ctx.INTLIT().getText()))

    # def visitMtype(self,ctx:MPParser.MtypeContext):
    #     return IntType()