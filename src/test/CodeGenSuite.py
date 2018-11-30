import unittest
from TestUtils import TestCodeGen
from AST import *


class CheckCodeGenSuite(unittest.TestCase):
    # def test_int(self):
    #     """Simple program: int main() {} """
    #     input = """procedure main(); begin putInt(100); end"""
    #     expect = "100"
    #     self.assertTrue(TestCodeGen.test(input,expect,500))
    # def test_int_ast(self):
    #     input = """
    #     var a:integer;
    #     procedure main();
    #     begin
    #         a := 5;
    #         putInt(a);
    #     end
    #     """
    #     expect = "5"
    #     self.assertTrue(TestCodeGen.test(input,expect,501))
    # def test3(self):
    #     input = """
    #     procedure main();
    #     begin
    #         putBool(True);
    #     end
    #     """
    #     expect = True
    #     self.assertTrue(TestCodeGen.test(input,expect,503))

    # def test4(self):
    #     input = """
    #     procedure main();
    #     begin
    #         putString("Phats");
    #     end
    #     """
    #     expect = "Phats"
    #     self.assertTrue(TestCodeGen.test(input,expect,504))
    
    # def test5(self):
    #     input = """
    #     procedure main();
    #     begin
    #         putFloat(-3.2);
    #     end
    #     """
    #     expect = "-3.2"
    #     self.assertTrue(TestCodeGen.test(input,expect,505))
    def test6(self):
        input = """
        procedure main();
        begin
            putBool(not True);
        end
        """
        expect = "false"
        self.assertTrue(TestCodeGen.test(input,expect,506))
