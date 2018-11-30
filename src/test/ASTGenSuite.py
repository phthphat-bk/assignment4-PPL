import unittest
from TestUtils import TestAST
from AST import *

class ASTGenSuite(unittest.TestCase):
    def test_simple_program(self):
        """Simple program: int main() {} """
        input = """
        procedure main();
        begin
            putBool(not True);
        end
        """
        expect = ""
        self.assertTrue(TestAST.test(input,expect,300))
   