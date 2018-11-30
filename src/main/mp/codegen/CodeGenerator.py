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
        return [Symbol("getInt", MType(list(), IntType()), CName(self.libName)),
                    Symbol("putInt", MType([IntType()], VoidType()), CName(self.libName)),
                    Symbol("putIntLn", MType([IntType()], VoidType()), CName(self.libName)),
                    Symbol("putFloat", MType([FloatType()], VoidType()), CName(self.libName)),
                    Symbol("putString", MType([StringType()], VoidType()), CName(self.libName)),
                    Symbol("putBool", MType([BoolType()], VoidType()), CName(self.libName))
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

        # Generate code for parameter declarations
        if isInit:
            self.emit.printout(self.emit.emitVAR(frame.getNewIndex(), "this", ClassType(self.className), frame.getStartLabel(), frame.getEndLabel(), frame))
            reduce(lambda y,x: self.visit(x, y),consdecl.param,SubBody(frame,list()))
        if isMain:
            self.emit.printout(self.emit.emitVAR(frame.getNewIndex(), "args", ArrayPointerType(StringType()), frame.getStartLabel(), frame.getEndLabel(), frame))

        body = consdecl.body
        self.emit.printout(self.emit.emitLABEL(frame.getStartLabel(), frame))

        # Generate code for statements
        if isInit:
            self.emit.printout(self.emit.emitREADVAR("this", ClassType(self.className), 0, frame))
            self.emit.printout(self.emit.emitINVOKESPECIAL(frame))
        list(map(lambda x: self.visit(x, SubBody(frame, glenv)), body))

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
        return SubBody(None, [Symbol(ast.name, MType(list(), ast.returnType), CName(self.className))] + subctxt.sym)

    def visitCallStmt(self, ast, o):
        #ast: CallStmt
        #o: Any

        ctxt = o
        frame = ctxt.frame
        nenv = ctxt.sym
        sym = self.lookup(ast.method.name, nenv, lambda x: x.name)
        cname = sym.value.value
    
        ctype = sym.mtype

        in_ = ("", list())
        for x in ast.param:
            str1, typ1 = self.visit(x, Access(frame, nenv, False, True))
            in_ = (in_[0] + str1, in_[1].append(typ1))
        self.emit.printout(in_[0])
        #print(ctype.partype)
        self.emit.printout(self.emit.emitINVOKESTATIC(cname + "/" + ast.method.name, ctype, frame))

    def visitId(self, ast, o):
        ctxt = o
        frame = ctxt.frame
        sym = self.lookup(ast.name, ctxt.sym,lambda x: x.name)
        if (ctxt.isLeft):
            if type(sym.value) is Index:
                return self.emit.emitWRITEVAR(sym.name, sym.mtype, sym.value.value, frame), sym.mtype
            else:
                return self.emit.emitPUTSTATIC(sym.value.value + '/' + sym.name, sym.mtype, frame), sym.mtype
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
        frame = ctxt.frame = ctxt.frame
        self.emit.printout(self.emit.emitATTRIBUTE(ast.variable.name,ast.varType,False,""))
        return SubBody(None, [Symbol(ast.variable.name, ast.varType, CName(self.className))] + ctxt.sym)       

    def visitUnaryOp(self,ast,o):
        ctxt = o
        frame = ctxt.frame
        exp, expType = self.visit(ast.body, o)
        #print(expType)
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
        # print(type(leftType) == IntType)

        if type(leftType) != type(rightType):
            if ast.op in ['+','-']:
                return (leftExp + self.emit.emitI2F(frame)) if type(leftType) == IntType else leftExp
                #return ((leftExp + self.emit.emitI2F(frame)) if type(leftType) == IntType else leftExp) + ((rightExp + self.emit.emitI2F(frame)) if type(rightType) == IntType else rightExp) + self.emit.emitADDOP(ast.op,FloatType(),frame), FloatType()
            if type(rightType) == IntType:
                    return leftExp + rightExp + self.emit.emitI2F(frame) + self.emit.emitADDOP(ast.op,FloatType(),frame), FloatType()
            else:
                if type(leftType) == IntType:
                    return leftExp + self.emit.emitI2F(frame) + rightExp + self.emit.emitMULOP(ast.op,FloatType(),frame), FloatType()
                if type(rightType) == IntType:
                    return leftExp + rightExp + self.emit.emitI2F(frame) + self.emit.emitMULOP(ast.op,FloatType(),frame), FloatType()
        else:            
            if type(leftType) == IntType:
                return leftExp + rightExp + self.emit.emitADDOP(ast.op,leftType,frame), leftType




























# '''
#  *   @author Nguyen Hua Phung
#  *   @version 1.0
#  *   23/10/2015
#  *   This file provides a simple version of code generator
#  *
# '''
# import sys
# import os
# sys.path.append(os.path.abspath('./../utils/'))
# from AST import *
# from Visitor import *

# from Utils import *
# from StaticCheck import *
# from StaticError import *
# from Emitter import Emitter
# from Frame import Frame
# from abc import ABC, abstractmethod
# from functools import reduce
# class CodeGenerator(Utils):
#     def __init__(self):
#         self.libName = "io"

#     def init(self):
#         return [Symbol("getInt", MType(list(), IntType()), CName(self.libName)),
#                     Symbol("putInt", MType([IntType()], VoidType()), CName(self.libName)),
#                     Symbol("putIntLn", MType([IntType()], VoidType()), CName(self.libName)),
#                     Symbol("putFloat", MType([FloatType()], VoidType()), CName(self.libName))
#                     ]

#     def gen(self, ast, dir_):
#         #ast: AST
#         #dir_: String

#         gl = self.init()
#         gc = CodeGenVisitor(ast, gl, dir_)
#         gc.visit(ast, None)

# # class StringType(Type):
    
# #     def __str__(self):
# #         return "StringType"

# #     def accept(self, v, param):
# #         return None

# class ArrayPointerType(Type):
#     def __init__(self, ctype):
#         #cname: String
#         self.eleType = ctype

#     def __str__(self):
#         return "ArrayPointerType({0})".format(str(self.eleType))

#     def accept(self, v, param):
#         return None
# class ClassType(Type):
#     def __init__(self,cname):
#         self.cname = cname
#     def __str__(self):
#         return "Class({0})".format(str(self.cname))
#     def accept(self, v, param):
#         return None       
# class SubBody():
#     def __init__(self, frame, sym, firstVisit = False):
#         #frame: Frame
#         #sym: List[Symbol]
#         self.frame = frame
#         self.sym = sym
#         self.firstVisit = firstVisit

# class Access():
#     def __init__(self, frame, sym, isLeft, isFirst):
#         #frame: Frame
#         #sym: List[Symbol]
#         #isLeft: Boolean
#         #isFirst: Boolean

#         self.frame = frame
#         self.sym = sym
#         self.isLeft = isLeft
#         self.isFirst = isFirst

# class Val(ABC):
#     pass

# class Index(Val):
#     def __init__(self, value):
#         #value: Int

#         self.value = value

# class CName(Val):
#     def __init__(self, value):
#         #value: String

#         self.value = value

# class CodeGenVisitor(BaseVisitor, Utils):
#     def __init__(self, astTree, env, dir_):
#         #astTree: AST
#         #env: List[Symbol]
#         #dir_: File

#         self.astTree = astTree
#         self.env = env
#         self.className = "MPClass"
#         self.path = dir_
#         self.emit = Emitter(self.path + "/" + self.className + ".j")

#     def visitProgram(self, ast, c):
#         #ast: Program
#         #c: Any
#         self.emit.printout(self.emit.emitPROLOG(self.className, "java.lang.Object"))
#         e = SubBody(None, self.env, True)
#         for x in ast.decl:
#             e = self.visit(x, e)

#         e.firstVisit = False
#         for x in ast.decl:
#             self.visit(x, e)
#         # generate default constructor
#         self.genMETHOD(FuncDecl(Id("<init>"), list(), list(), list(),None), c, Frame("<init>", VoidType))
#         self.emit.emitEPILOG()
#         return c

#     def genMETHOD(self, consdecl, o, frame):
#         #consdecl: FuncDecl
#         #o: Any
#         #frame: Frame

#         isInit = consdecl.returnType is None
#         isMain = consdecl.name.name == "main" and len(consdecl.param) == 0 and type(consdecl.returnType) is VoidType
#         returnType = VoidType() if isInit else consdecl.returnType
#         methodName = "<init>" if isInit else consdecl.name.name
#         intype = [ArrayPointerType(StringType())] if isMain else list()
#         mtype = MType(intype, returnType)

#         self.emit.printout(self.emit.emitMETHOD(methodName, mtype, not isInit, frame))

#         frame.enterScope(True)

#         glenv = o

#         # Generate code for parameter declarations
#         if isInit:
#             self.emit.printout(self.emit.emitVAR(frame.getNewIndex(), "this", ClassType(self.className), frame.getStartLabel(), frame.getEndLabel(), frame))
#             reduce(lambda y,x: self.visit(x, y),consdecl.param,SubBody(frame,list()))
#         if isMain:
#             self.emit.printout(self.emit.emitVAR(frame.getNewIndex(), "args", ArrayPointerType(StringType()), frame.getStartLabel(), frame.getEndLabel(), frame))

#         body = consdecl.body
#         self.emit.printout(self.emit.emitLABEL(frame.getStartLabel(), frame))
#         #Generate code for local var declarations
#         #list(map())

#         # Generate code for statements
#         if isInit:
#             self.emit.printout(self.emit.emitREADVAR("this", ClassType(self.className), 0, frame))
#             self.emit.printout(self.emit.emitINVOKESPECIAL(frame))
#         list(map(lambda x: self.visit(x, SubBody(frame, glenv)), body))

#         self.emit.printout(self.emit.emitLABEL(frame.getEndLabel(), frame))
#         if type(returnType) is VoidType:
#             self.emit.printout(self.emit.emitRETURN(VoidType(), frame))
#         self.emit.printout(self.emit.emitENDMETHOD(frame))
#         frame.exitScope()

#     def visitFuncDecl(self, ast, o):
#         #ast: FuncDecl
#         #o: Any
        
#         subctxt = o
#         if(subctxt.firstVisit):
#             return SubBody(None, [Symbol(ast.name.name, MType(list(), ast.returnType), CName(self.className))] + subctxt.sym, True)
#         frame = Frame(ast.name, ast.returnType)
#         self.genMETHOD(ast, subctxt.sym, frame)

#     def visitCallStmt(self, ast, o):
#         #ast: CallStmt
#         #o: Any

#         ctxt = o
#         frame = ctxt.frame
#         nenv = ctxt.sym
#         sym = self.lookup(ast.method.name, nenv, lambda x: x.name)
#         cname = sym.value.value
    
#         ctype = sym.mtype

#         in_ = ("", list())
#         for x in ast.param:
#             str1, typ1 = self.visit(x, Access(frame, nenv, False, True))
#             in_ = (in_[0] + str1, in_[1].append(typ1))
#         self.emit.printout(in_[0])
#         self.emit.printout(self.emit.emitINVOKESTATIC(cname + "/" + ast.method.name, ctype, frame))

#     def visitIntLiteral(self, ast, o):
#         #ast: IntLiteral
#         #o: Any

#         ctxt = o
#         frame = ctxt.frame
#         return self.emit.emitPUSHICONST(ast.value, frame), IntType()

#     def visitId(self, ast, o):
#         ctxt = o
#         frame = ctxt.frame
#         sym = self.lookup(ast.name, ctxt.sym,lambda x: x.name)
#         if (ctxt.isLeft):
#             if type(sym.value) is Index:
#                 return self.emit.emitWRITEVAR(sym.name, sym.mtype, sym.value.value, frame), sym.mtype
#             else:
#                 return self.emit.emitPUTSTATIC(sym.value.value + '/' + sym.name, sym.mtype, frame), sym.mtype
#         else:
#             return self.emit.emitGETSTATIC(sym.value.value + '/' + sym.name, sym.mtype, frame), sym.mtype

#     def visitAssign(self, ast, o):
#         #lhs:Expr
#         #exp:Expr
#         ctxt = o
#         frame = ctxt.frame
#         rhs = self.visit(ast.exp, Access(frame, ctxt.sym, False,""))[0]
#         lhs = self.visit(ast.lhs, Access(frame, ctxt.sym, True,""))[0]
#         self.emit.printout(rhs + lhs)
#         return


#     def visitFloatLiteral(self, ast, o):
#         #ast: FloatLiteral
#         #o: Any
#         ctxt = o
#         frame = ctxt.frame
#         return self.emit.emitPUSHFCONST(str(ast.value), frame), FloatType()

#     def visitVarDecl(self, ast, o):
#         ctxt = o
#         frame = ctxt.frame
#         #print(frame)
#         if (ctxt.firstVisit):
#             return SubBody(None, [Symbol(ast.variable.name, ast.varType, CName(self.className))] + ctxt.sym,True)       
#         if (frame): #para or local variable
#             print(frame)
#             idx = frame.getNewIndex
#             self.emit.printout(self.emit.emitVAR(idx, ast.variable.name,ast.varType,frame.getStartLabel(),frame.getEndLabel(), frame))
#             return SubBody(frame,Symbol(ast.variable.name,ast.varType,Index(idx)) + ctxt.sym)
#         else:
#             self.emit.printout(self.emit.emitATTRIBUTE(ast.variable.name,ast.varType,False,""))

#     def visitBinaryOp(self, ast, o):
#         #op:string: AND THEN => andthen; OR ELSE => orelse; other => keep it
#         #left:Expr
#         #right:Expr

#         ctxt = o
#         frame = ctxt.frame

#         leftExp, leftType = self.visit(ast.left, o)
#         rightExp, rightType = self.visit(ast.right, o)

#         if type(leftType) != type(rightType):
#             if ast.op in ['+','-']:
#                 return (leftExp + self.emit.emitI2F(frame)) if type(leftType) == IntType else leftExp
#                 #return ((leftExp + self.emit.emitI2F(frame)) if type(leftType) == IntType else leftExp) + ((rightExp + self.emit.emitI2F(frame)) if type(rightType) == IntType else rightExp) + self.emit.emitADDOP(ast.op,FloatType(),frame), FloatType()
#             if type(rightType) == IntType:
#                     return leftExp + rightExp + self.emit.emitI2F(frame) + self.emit.emitADDOP(ast.op,FloatType(),frame), FloatType()
#             else:
#                 if type(leftType) == IntType:
#                     return leftExp + self.emit.emitI2F(frame) + rightExp + self.emit.emitMULOP(ast.op,FloatType(),frame), FloatType()
#                 if type(rightType) == IntType:
#                     return leftExp + rightExp + self.emit.emitI2F(frame) + self.emit.emitMULOP(ast.op,FloatType(),frame), FloatType()
#         else:            
#             if type(leftType) == IntType:
#                 return leftExp + rightExp + self.emit.emitADDOP(ast.op,leftType,frame), leftType

