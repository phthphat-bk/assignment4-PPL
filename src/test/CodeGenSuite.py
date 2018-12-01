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
    # def test6(self):
    #     input = """
    #     procedure main();
    #     begin
    #         putBool(not True);
    #     end
    #     """
    #     expect = "false"
    #     self.assertTrue(TestCodeGen.test(input,expect,506))
    # def test7(self):
    #     input = """
    #     //var a: integer;
    #     //function phat():integer;
    #     //begin
    #     //    a := 5;
    #     //end
    #     //var a:integer;
    #     procedure main();
    #     begin
    #         putInt(6 div 2);
    #     end
    #     """
    #     expect = "-2"
    #     self.assertTrue(TestCodeGen.test(input,expect,507))
    # def test8(self):
    #     input = """
    #     procedure main();
    #     var x: integer;
    #     begin
    #         x := (5 mod 2);
    #         putInt(x); 
    #     end
    #     """
    #     expect = "1"
    #     self.assertTrue(TestCodeGen.test(input,expect,508))
    # def test9(self):
    #     input = """
    #     var a: integer;
    #     function phat():integer;
    #     begin
    #         a := 5;
    #         return 0;
    #     end
    #     procedure main();
    #     begin 
    #         a := 3;
    #         putInt(a);
    #     end
    #     """
    #     expect = "3"
    #     self.assertTrue(TestCodeGen.test(input,expect,509))