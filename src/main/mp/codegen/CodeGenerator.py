#CodeGenaration
'''
 *   @author Nguyen Hua Phung
 *   @version 1.0
 *   23/10/2015
 *   This file provides a simple version of code generator
 *
'''
import sys
import os
sys.path.append(os.path.abspath('./../utils/'))
from AST import *
from Visitor import *

from Utils import *
from StaticCheck import *
from StaticError import *
from Emitter import Emitter
from Frame import Frame
from abc import ABC, abstractmethod
from functools import reduce
class CodeGenerator(Utils):
    def __init__(self):
        self.libName = "io"

    def init(self):
        return [Symbol("getInt",MType([],IntType()), CName(self.libName)),
    			   Symbol("putIntLn",MType([IntType()],VoidType()), CName(self.libName)),
                   Symbol("putInt", MType([IntType()], VoidType()), CName(self.libName)),
                   Symbol("getFloat", MType([], FloatType()), CName(self.libName)),
                   Symbol("putFloat", MType([FloatType()], VoidType()), CName(self.libName)),
                   Symbol("putFloatLn", MType([FloatType()], VoidType()), CName(self.libName)),
                   Symbol("putBool", MType([BoolType()], VoidType()), CName(self.libName)),
                   Symbol("putBoolLn", MType([BoolType()], VoidType()), CName(self.libName)),
                   Symbol("putString", MType([StringType()], VoidType()), CName(self.libName)),
                   Symbol("putStringLn", MType([StringType()], VoidType()), CName(self.libName)),
                   Symbol("putLn", MType([], VoidType()), CName(self.libName))
        ]

    def gen(self, ast, dir_):
        #ast: AST
        #dir_: String

        gl = self.init()
        gc = CodeGenVisitor(ast, gl, dir_)
        gc.visit(ast, None)

# class StringType(Type):
#     def __str__(self):
#         return "StringType"

#     def accept(self, v, param):
#         return None

class ArrayPointerType(Type):
    def __init__(self, ctype):
        #cname: String
        self.eleType = ctype

    def __str__(self):
        return "ArrayPointerType({0})".format(str(self.eleType))

    def accept(self, v, param):
        return None
class ClassType(Type):
    def __init__(self,cname):
        self.cname = cname
    def __str__(self):
        return "Class({0})".format(str(self.cname))
    def accept(self, v, param):
        return None       
class SubBody():
    def __init__(self, frame, sym):
        #frame: Frame
        #sym: List[Symbol]

        self.frame = frame
        self.sym = sym
class Access():
    def __init__(self, frame, sym, isLeft, isFirst):
        #frame: Frame
        #sym: List[Symbol]
        #isLeft: Boolean
        #isFirst: Boolean

        self.frame = frame
        self.sym = sym
        self.isLeft = isLeft
        self.isFirst = isFirst
class Val(ABC):
    pass
class Index(Val):
    def __init__(self, value):
        #value: Int

        self.value = value
class CName(Val):
    def __init__(self, value):
        #value: String

        self.value = value

class CodeGenVisitor(BaseVisitor, Utils):
    def __init__(self, astTree, env, dir_):
        #astTree: AST
        #env: List[Symbol]
        #dir_: File

        self.astTree = astTree
        self.env = env
        self.className = "MPClass"
        self.path = dir_
        self.emit = Emitter(self.path + "/" + self.className + ".j")

    def visitProgram(self, ast, c):
        #ast: Program
        #c: Any

        self.emit.printout(self.emit.emitPROLOG(self.className, "java.lang.Object"))
        e = SubBody(None, self.env)
        for x in ast.decl:
            e = self.visit(x, e)
        # generate default constructor
        self.genMETHOD(FuncDecl(Id("<init>"), list(), list(), list(),None), c, Frame("<init>", VoidType))
        self.emit.emitEPILOG()
        return c

    def genMETHOD(self, consdecl, o, frame):
        #consdecl: FuncDecl
        #o: Any
        #frame: Frame
        isInit = consdecl.returnType is None
        isMain = consdecl.name.name == "main" and len(consdecl.param) == 0 and type(consdecl.returnType) is VoidType
        returnType = VoidType() if isInit else consdecl.returnType
        methodName = "<init>" if isInit else consdecl.name.name
        intype = [ArrayPointerType(StringType())] if isMain else list()
        mtype = MType(intype, returnType)

        self.emit.printout(self.emit.emitMETHOD(methodName, mtype, not isInit, frame))

        frame.enterScope(True)
        
        glenv = o
        env = SubBody(frame,glenv)
        #print(env.sym[0].name)

        # Generate code for parameter declarations
        if isInit:
            self.emit.printout(self.emit.emitVAR(frame.getNewIndex(), "this", ClassType(self.className), frame.getStartLabel(), frame.getEndLabel(), frame))
        if isMain:
            self.emit.printout(self.emit.emitVAR(frame.getNewIndex(), "args", ArrayPointerType(StringType()), frame.getStartLabel(), frame.getEndLabel(), frame))
        else:
            for x in consdecl.param:
                env = self.visit(x, env)
        for x in consdecl.local:
            env = self.visit(x, env)

        body = consdecl.body
        self.emit.printout(self.emit.emitLABEL(frame.getStartLabel(), frame))

        if isInit:
            self.emit.printout(self.emit.emitREADVAR("this", ClassType(self.className), 0, frame))
            self.emit.printout(self.emit.emitINVOKESPECIAL(frame))
        list(map(lambda x: self.visit(x, env), body))

        self.emit.printout(self.emit.emitLABEL(frame.getEndLabel(), frame))
        if type(returnType) is VoidType:
            self.emit.printout(self.emit.emitRETURN(VoidType(), frame))
        self.emit.printout(self.emit.emitENDMETHOD(frame))
        frame.exitScope()

    def visitFuncDecl(self, ast, o):
        #ast: FuncDecl
        #o: Any

        subctxt = o
        frame = Frame(ast.name, ast.returnType)
        self.genMETHOD(ast, subctxt.sym, frame)

        #print(ast.name.name)
        return SubBody(None, [Symbol(ast.name.name, MType(list(), ast.returnType), CName(self.className))] + subctxt.sym)

    def visitCallStmt(self, ast, o):
        #ast: CallStmt
        #o: Any

        ctxt = o
        frame = ctxt.frame
        nenv = ctxt.sym
        sym = self.lookup(ast.method.name.lower(), nenv, lambda x: x.name.lower())
        cname = sym.value.value
    
        ctype = sym.mtype

        in_ = ("", list())
        L = zip(ast.param, ctype.partype)
        #print(ctype.partype)
        for x in L:
            str1, typ1 = self.visit(x[0], Access(frame, nenv, False, True))

            in_ = (in_[0] + str1 + (self.emit.emitI2F(frame) if type(typ1) is IntType and type(x[1]) is FloatType else ""), in_[1] + [typ1] )
        self.emit.printout(in_[0])
        self.emit.printout(self.emit.emitINVOKESTATIC(cname + "/" + ast.method.name, ctype, frame))

    def visitCallExpr(self, ast, o):
        #ast: CallExpr
        #o: Any

        ctxt = o
        frame = ctxt.frame
        nenv = ctxt.sym
        sym = self.lookup(ast.method.name.lower(), nenv, lambda x: x.name.lower())
        cname = sym.value.value
    
        ctype = sym.mtype

        in_ = ("", list())
        L = zip(ast.param, ctype.partype)
        #print(ctype.partype)
        for x in L:
            str1, typ1 = self.visit(x[0], Access(frame, nenv, False, True))
            in_ = (in_[0] + str1 + (self.emit.emitI2F(frame) if type(typ1) is IntType and type(x[1]) is FloatType else ""), in_[1] + [typ1] )
        # self.emit.printout(in_[0])
        # self.emit.printout(self.emit.emitINVOKESTATIC(cname + "/" + ast.method.name, ctype, frame))
        return in_[0] + self.emit.emitINVOKESTATIC(cname+"/"+ast.method.name,ctype,frame),ctype.rettype

    def visitId(self, ast, o):
        ctxt = o
        frame = ctxt.frame
        # print(ctxt.sym[0].name)
        sym = self.lookup(ast.name, ctxt.sym,lambda x: x.name)
        if (ctxt.isLeft):
            if type(sym.value) is Index:
                return self.emit.emitWRITEVAR(sym.name, sym.mtype, sym.value.value, frame), sym.mtype
            else:
                return self.emit.emitPUTSTATIC(sym.value.value + '/' + sym.name, sym.mtype, frame), sym.mtype
        else:
            if type(sym.value) is Index:
                return self.emit.emitREADVAR(sym.name, sym.mtype, sym.value.value, frame), sym.mtype
            else:
                return self.emit.emitGETSTATIC(sym.value.value + '/' + sym.name, sym.mtype, frame), sym.mtype

    def visitAssign(self, ast, o):
        #lhs:Expr
        #exp:Expr
        ctxt = o
        frame = ctxt.frame
        rhs = self.visit(ast.exp, Access(frame, ctxt.sym, False,""))[0]
        lhs = self.visit(ast.lhs, Access(frame, ctxt.sym, True,""))[0]
        self.emit.printout(rhs + lhs)
        return

    def visitIf(self, ast, o):
        ctxt = o
        frame = ctxt.frame
        env = ctxt.sym
        hasElse = len(ast.elseStmt) != 0
        exp, expType = self.visit(ast.expr, Access(frame, env, False,""))
        elseLabel = frame.getNewLabel()
        nextLabel = frame.getNewLabel() if hasElse else elseLabel
        self.emit.printout(exp + self.emit.emitIFFALSE(elseLabel, frame))
        for stmt in ast.thenStmt:
            self.visit(stmt, SubBody(frame, env))
        self.emit.printout(self.emit.emitGOTO(nextLabel,frame))
        self.emit.printout(self.emit.emitLABEL(elseLabel, frame))
        for stmt in ast.elseStmt:
            self.visit(stmt, SubBody(frame, env))
        if hasElse:
            self.emit.printout(self.emit.emitLABEL(nextLabel, frame))
    
    def visitBreak(self, ast, o):
        frame = o.frame
        self.emit.printout(self.emit.emitGOTO(frame.getBreakLabel(), frame))
    def visitContinue(self, ast, o):
        frame = o.frame
        self.emit.printout(self.emit.emitGOTO(frame.getContinueLabel(), frame))
    
    def visitReturn(self, ast, o):
        ctxt = o
        frame = ctxt.frame
        env = ctxt.sym
        if ast.expr is None:
            self.emit.printout(self.emit.emitRETURN(VoidType(), frame))
        else:
            str1, typ1 = self.visit(ast.expr, Access(frame, env,False,""))
            self.emit.printout(str1)
            if (type(frame.returnType) == FloatType and type(typ1) == IntType):
                self.emit.printout(self.emit.emitI2F(frame))
            self.emit.printout(self.emit.emitRETURN(frame.returnType,frame))

    def visitWhile(self,ast,o):
        frame=o.frame
        frame.enterLoop()
        label1=frame.getContinueLabel()
        label2=frame.getBreakLabel()
        code=self.emit.emitLABEL(label1,frame)
        code+=self.visit(ast.exp,Access(frame,o.sym,False,True))[0]
        code+=self.emit.emitIFFALSE(label2,frame)
        self.emit.printout(code)
        
        list(map(lambda x:self.visit(x,o),ast.sl))
        
        code=self.emit.emitGOTO(str(label1),frame)
        code+=self.emit.emitLABEL(label2,frame)
        self.emit.printout(code)
        frame.exitLoop()

    def visitFor(self,ast,o):
        frame=o.frame
        label1=frame.getNewLabel()
        #label2=frame.getNewLabel()
        frame.enterLoop()
        conlabel=frame.getContinueLabel()
        breaklabel=frame.getBreakLabel()
        code=self.visit(ast.expr1,Access(frame,o.sym,False,""))[0]
        code+=self.visit(ast.id,Access(frame,o.sym,True,True))[0]
        code+=self.emit.emitLABEL(label1,frame)
        code+=self.visit(ast.id,Access(frame,o.sym,False,True))[0]
        code+=self.visit(ast.expr2,Access(frame,o.sym,False,""))[0]

        op='<=' if ast.up else '>='
        code+=self.emit.emitRELOP(op,IntType(),label1,breaklabel,frame)
        self.emit.printout(code)

        list(map(lambda x:self.visit(x,o),ast.loop))
        
        
        op='+' if ast.up else '-'
        code=self.emit.emitLABEL(conlabel,frame)
        code+=self.visit(ast.id,Access(frame,o.sym,False,True))[0]
        code+=self.visit(IntLiteral(1),o)[0]
        code+=self.emit.emitADDOP(op,IntType(),frame)
        code+=self.visit(ast.id,Access(frame,o.sym,True,True))[0]
        code+=self.emit.emitGOTO(str(label1),frame)
        code+=self.emit.emitLABEL(breaklabel,frame)
        self.emit.printout(code)
        frame.exitLoop()

    def visitWith(self,ast,o):
        frame=o.frame
        frame.enterScope(False)
        e=SubBody(frame,[])
        for x in ast.decl:
            e=self.visit(x,e)
        self.emit.printout(self.emit.emitLABEL(frame.getStartLabel(),frame))
        
        arraySym=list(filter(lambda x:isinstance(x.mtype,ArrayType),e.sym))
        codelist=list(map(lambda x:self.visit(IntLiteral(x.mtype.upper-x.mtype.lower+1),e)[0]
                            +self.emit.emitNEW(x.mtype.eleType,frame)
                            +self.emit.emitWRITEVAR(x.name,ArrayPointerType(x.mtype.eleType),x.value.value,e.frame),
                            arraySym))
        #if codelist !=[]:
        code=reduce(lambda x,y:x+y,codelist,"")
        self.emit.printout(code)        

        o=SubBody(frame,e.sym+o.sym)
        list(map(lambda x:self.visit(x,o),ast.stmt))
        self.emit.printout(self.emit.emitLABEL(frame.getEndLabel(),frame))
        frame.exitScope()

    def visitFloatLiteral(self, ast, o):
        #ast: FloatLiteral
        #o: Any
        ctxt = o
        frame = ctxt.frame
        return self.emit.emitPUSHFCONST(str(ast.value), frame), FloatType()

    def visitIntLiteral(self, ast, o):
        #ast: IntLiteral
        #o: Any

        ctxt = o
        frame = ctxt.frame
        return self.emit.emitPUSHICONST(ast.value, frame), IntType()

    def visitStringLiteral(self, ast, o):
        ctxt = o
        frame = ctxt.frame
        return self.emit.emitPUSHCONST(str(ast.value), StringType(), frame), StringType()

    def visitBooleanLiteral(self, ast, o):
        #ast: FloatLiteral
        #o: Any
        ctxt = o
        frame = ctxt.frame
        return self.emit.emitPUSHICONST(str(ast.value),frame), BoolType()

    def visitVarDecl(self, ast, o):
        ctxt = o
        frame = ctxt.frame
        if frame is None: 
            self.emit.printout(self.emit.emitATTRIBUTE(ast.variable.name,ast.varType,False,""))
            return SubBody(None, [Symbol(ast.variable.name, ast.varType, CName(self.className))] + ctxt.sym)
        else: #parameter or local variable
            self.emit.printout(self.emit.emitVAR(frame.getNewIndex(), ast.variable.name,ast.varType, frame.getStartLabel(),frame.getEndLabel(),frame))
            return SubBody(frame, [Symbol(ast.variable.name, ast.varType, Index(frame.getCurrIndex() - 1))] + ctxt.sym)


    def visitUnaryOp(self,ast,o):
        ctxt = o
        frame = ctxt.frame
        exp, expType = self.visit(ast.body, o)
        if ast.op == '-':
            return exp + self.emit.emitNEGOP(expType, frame), expType
        elif ast.op == 'not':
            return exp + self.emit.emitNOT(expType,frame), expType

    def visitBinaryOp(self, ast, o):
        #op:string: AND THEN => andthen; OR ELSE => orelse; other => keep it
        #left:Expr
        #right:Expr

        ctxt = o
        frame = ctxt.frame

        leftExp, leftType = self.visit(ast.left, o)
        rightExp, rightType = self.visit(ast.right, o)
        if type(leftType) != type(rightType):
            if type(leftType) == IntType:
                leftExp += self.emit.emitI2F(frame)
            if type(rightType) == IntType:
                rightExp += self.emit.emitI2F(frame)
            if ast.op in ['+', '-']:
                return leftExp + rightExp + self.emit.emitADDOP(ast.op,FloatType(),frame), FloatType()
            elif ast.op in ['*','/']:
                return leftExp + rightExp + self.emit.emitMULOP(ast.op,FloatType(),frame), FloatType()
            elif ast.op in ['<','>','>=','<=','=', '<>']:
                return leftExp + rightExp + self.emit.emitREOP(ast.op, leftType, frame), BoolType()

        else:            
            if ast.op in ['+','-']:
                return leftExp + rightExp + self.emit.emitADDOP(ast.op,leftType,frame), leftType
            elif ast.op == '*':
                return leftExp + rightExp + self.emit.emitMULOP(ast.op,leftType,frame), leftType
            elif ast.op == '/':
                if type(leftType) == IntType:
                    return leftExp + self.emit.emitI2F(frame) + rightExp + self.emit.emitI2F(frame) + self.emit.emitMULOP(ast.op,FloatType(),frame), FloatType()
                else:
                    return leftExp + rightExp + self.emit.emitMULOP(ast.op,FloatType(),frame), FloatType()
            elif ast.op.lower() == 'or':
                return leftExp + rightExp + self.emit.emitOROP(frame), BoolType()
            elif ast.op.lower() == 'and':
                return leftExp + rightExp + self.emit.emitANDOP(frame), BoolType()
            elif ast.op.lower() == 'mod':
                return leftExp + rightExp + self.emit.emitMOD(frame), IntType()
            elif ast.op.lower() == 'div':
                return leftExp + rightExp + self.emit.emitDIV(frame), IntType()
            elif ast.op in ['<','>','>=','<=','=', '<>']:
                if type(leftType) == IntType:
                    leftExp += self.emit.emitI2F(frame)
                if type(rightType) == IntType:
                    rightExp += self.emit.emitI2F(frame)
                return leftExp + rightExp + self.emit.emitREOP(ast.op, leftType, frame), BoolType()
            
        # if ast.op in [">" , "<" , ">=" , "<=", "<>","="]:
        #     if type(leftType) is FloatType and type(rightType) is IntType:
        #         return leftExp + rightExp + self.emit.emitI2F(frame) + self.emit.emitREOP(ast.op, leftType, frame), BoolType
        #     elif type(leftType) is IntType and type(rightType) is FloatType:
        #         return leftExp + self.emit.emitI2F(frame) + rightExp + self.emit.emitREOP(ast.op, rightType, frame), BoolType
        #     else:
        #         return leftExp + rightExp + self.emit.emitREOP(ast.op, leftType, frame), BoolType       
        # if ast.op == "div" :
        #     return leftExp + rightExp + self.emit.emitDIV( frame), leftType
        # if ast.op == "mod" :
        #     return leftExp + rightExp + self.emit.emitMOD( frame), leftType
        # if ast.op == "and" :
        #     return leftExp + rightExp + self.emit.emitANDOP( frame), leftType
        # if ast.op == "or" :
        #     return leftExp + rightExp + self.emit.emitOROP( frame), leftType



