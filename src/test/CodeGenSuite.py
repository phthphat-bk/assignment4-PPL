import unittest
from TestUtils import TestCodeGen
from AST import *


class CheckCodeGenSuite(unittest.TestCase):
    def test_int(self):
        """Simple program: int main() {} """
        input = """procedure main(); begin putInt(100); end"""
        expect = "100"
        self.assertTrue(TestCodeGen.test(input,expect,500))
    def test_int_ast(self):
        input = """
        var a:integer;
        procedure main();
        begin
            a := 5;
            putInt(a);
        end
        """
        expect = "5"
        self.assertTrue(TestCodeGen.test(input,expect,501))
    def test3(self):
        input = """
        procedure main();
        begin
            putBool(True);
        end
        """
        expect = "true"
        self.assertTrue(TestCodeGen.test(input,expect,503))

    def test4(self):
        input = """
        procedure main();
        begin
            putString("Phats");
        end
        """
        expect = "Phats"
        self.assertTrue(TestCodeGen.test(input,expect,504))
    
    def test5(self):
        input = """
        procedure main();
        begin
            putFloat(-3.2);
        end
        """
        expect = "-3.2"
        self.assertTrue(TestCodeGen.test(input,expect,505))
    def test6(self):
        input = """
        procedure main();
        begin
            putBool(not True);
        end
        """
        expect = "false"
        self.assertTrue(TestCodeGen.test(input,expect,506))
    def test7(self):
        input = """
        //var a: integer;
        //function phat():integer;
        //begin
        //    a := 5;
        //end
        //var a:integer;
        procedure main();
        begin
            putInt(6 div 2);
        end
        """
        expect = "3"
        self.assertTrue(TestCodeGen.test(input,expect,507))
    def test8(self):
        input = """
        procedure main();
        var x: integer;
        begin
            x := (5 mod 2);
            putInt(x); 
        end
        """
        expect = "1"
        self.assertTrue(TestCodeGen.test(input,expect,508))
    
    def test9(self):
        input = """
        var a: integer;
        function phat():integer;
        begin
            a := 5;
            return 0;
        end
        procedure main();
        begin 
            a := 3;
            putInt(a);
        end
        """
        expect = "3"
        self.assertTrue(TestCodeGen.test(input,expect,509))

    def test10(self):
        input = """
        procedure main();
        begin 
            putBool(3.0 < 2.0);
        end
        """
        expect = "false"
        self.assertTrue(TestCodeGen.test(input,expect,510))
    def test11(self):
        input = """
        function phat():integer;
        begin
            return 3;
        end
        procedure main();
        begin 
            putBool(3.0 < 2.0);
        end
        """
        expect = "false"
        self.assertTrue(TestCodeGen.test(input,expect,511))
    def test12(self):
        input = """
        function phat():real;
        begin
            return 3;
        end
        procedure main();
        begin 
            putBool(3.0 < 2.0);
        end
        """
        expect = "false"
        self.assertTrue(TestCodeGen.test(input,expect,512))
    
    def test13(self):
        input = """
        function phat():boolean;
        begin
            return true;
        end
        procedure main();
        begin 
            putBool(3.0 < 2.0);
        end
        """
        expect = "false"
        self.assertTrue(TestCodeGen.test(input,expect,513))
    
    def test14(self):
        input = """
        function phat():string;
        begin
            return "Phat";
        end
        procedure main();
        begin
            putBool(3.0 < 2.0);
        end
        """
        expect = "false"
        self.assertTrue(TestCodeGen.test(input,expect,514))
    
    def test14(self):
        input = """
        function phat():string;
        begin
            return "Phat";
        end
        procedure main();
        begin
            if false then putBool(3.0 < 2.0);
        end
        """
        expect = ""
        self.assertTrue(TestCodeGen.test(input,expect,514))
    
    def test15(self):
        input = """
        procedure main();
        begin
            if false then putBool(3.0 < 2.0);
            else
                putInt(3);
        end
        """
        expect = "3"
        self.assertTrue(TestCodeGen.test(input,expect,515))
    
    def test16(self):
        input = """
        procedure main();
        begin
            if 3 < 2 then putBool(3.0 < 2.0);
            else
                putInt(3);
        end
        """
        expect = "3"
        self.assertTrue(TestCodeGen.test(input,expect,516))
    
    def test17(self):
        input = """
        procedure main();
        begin
            if 3.0 < 2 then putBool(3.0 < 2.0);
            else
                putInt(3);
        end
        """
        expect = "3"
        self.assertTrue(TestCodeGen.test(input,expect,516))
    def test18(self):
        input = """
        procedure main();
        begin
            if 3.0 > 2 then putBool(3.0 < 2.0);
            else
                putInt(3);
        end
        """
        expect = "false"
        self.assertTrue(TestCodeGen.test(input,expect,518))
    def test19(self):
        input = """
        procedure main();
        var i:integer;
        begin
            i := 1;
            while (i < 5) do
            begin
                putInt(i);
                if i = 3 then break;
                i:=i+1;
            end
            //if i = 3 then putString("hihi");
        end
        """
        expect = "123"
        self.assertTrue(TestCodeGen.test(input,expect,519))
    def test20(self):
        input = """
        procedure print();
        begin
            putInt(3);
        end
        procedure main();
        begin
            print();
        end

        """
        expect = "3"
        self.assertTrue(TestCodeGen.test(input,expect,520))
    def test21(self):
        input = """
        procedure print();
        begin
            if true then return;
        end
        procedure main();
        begin
            print();
        end

        """
        expect = ""
        self.assertTrue(TestCodeGen.test(input,expect,521))
    def test22(self):
        input = """
        function phat():integer;
        begin
            if true then return 3;
            return 5;
        end
        procedure main();
        begin
            putInt(phat());
        end
        """
        expect = "3"
        self.assertTrue(TestCodeGen.test(input,expect,522))
    
    def test23(self):
        input = """
        var i,a,b:integer;
        procedure main();
        begin
            a := 1;
            for i := 1 to 2 do
                putInt(a);
        end
        """
        expect = "11"
        self.assertTrue(TestCodeGen.test(input, expect, 523))

    def test24(self):
        input = """
        var x:integer;
        procedure main();
        begin
            x := 1;
            foo(x, 1.0);
            putInt(x);
        end
        procedure foo(i: integer; f: real);
        var bar:boolean;
        begin
            bar := true;
            putBool(bar);
            i := 2;
            putInt(i);
        end
        """
        expect = "true21"
        self.assertTrue(TestCodeGen.test(input, expect, 524))
    def test25(self):
        input = """
        procedure main();
        begin
            putFloatLn(-2/5);
            putIntLn((27 mod 8));
            putIntLn(27 div -3);
            putInt(-28 div -3);
        end
		"""
        expect = "-0.4\n3\n-9\n9"
        self.assertTrue(TestCodeGen.test(input, expect, 525))

    def test26(self):
        input = """
        procedure main();
        begin
            putBool(not true);
            putBool(not false);
            putBool(not not true);
            putBool(not not false);
            putBool(not not not not (true and true));
        end
		"""
        expect = "falsetruetruefalsetrue"
        self.assertTrue(TestCodeGen.test(input, expect, 526))

    def test27(self):
        input = """
        var a : integer;
        procedure main();
        begin
            a := -4;
            putBool(a = a);
            putBool(a = a*1.0);
        end
        """
        expect = "truetrue"
        self.assertTrue(TestCodeGen.test(input, expect, 527))

    def test28(self):
        input = """
        procedure main();
        begin
            if 10 = 10 then
            begin
                putString("10 = 10"); 
            end
            else
                putString("10 <> 10");
        end
        """
        expect = "10 = 10"
        self.assertTrue(TestCodeGen.test(input, expect, 528))
    def test29(self):
        input = """
        procedure main();
        var b : BOOLEAN;
        begin
            b := true;
            while b do
            begin
                b := not b;
                putBool(b);
            end
        end
        """
        expect = "false"
        self.assertTrue(TestCodeGen.test(input, expect, 529))
    

    # def test_binop_508(self):
    #     input = """
	# 	procedure main();
	# 	begin
    #         // same result as AND
	# 		putBoolLn(true and then false);
    #         putBoolLn(true and then true);
    #         putBoolLn(false and then true);
    #         putBoolLn(false and then false);
    #         // skip evaluation of the second operand --> no error
    #         putBoolLn(false and then 0 div 0 = 0);
    #         // error
    #         // putBoolLn(true and then 0 div 0 = 0);
	# 		return;
	# 	end
	# 	"""
    #     expect = "false\ntrue\nfalse\nfalse\nfalse\n"
    #     self.assertTrue(TestCodeGen.test(input, expect, 508))

    