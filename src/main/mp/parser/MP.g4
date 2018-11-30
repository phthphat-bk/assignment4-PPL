grammar MP;

@lexer::header {
from lexererr import *
}

options {
	language = Python3;
}

program: declar+ EOF;
declar: varDeclar | funcDeclar | procDeclar; //assignStatement for testing
mptype: INTTYPE;

LB: '(';
RB: ')';
LP: '{';
RP: '}';
SEMI: ';';
COMMA: ',';
LS: '[';
RS: ']';
COLON: ':';
DOUBLEDOT: '..';
ASSIGN: ':=';
WS: [ \t\r\n]+ -> skip; // skip spaces, tabs, newlines
comment: TRADITIONALBLOCKCOMMENT | BLOCKCOMMENT | LINECOMMENT;
TRADITIONALBLOCKCOMMENT:
	'(*' (TRADITIONALBLOCKCOMMENT | .)*? '*)' -> skip;
BLOCKCOMMENT: LP .*? RP -> skip;
LINECOMMENT: '//' .*? '\n' -> skip;
ADD: '+';
SUB: '-';
MUL: '*';
DIVISION: '/';
DIV: D I V;
MOD: M O D;
NOT: N O T;
OR: O R;
AND: A N D;
EQUAL: '=';
NOTEQUAL: '<>';
LESS: '<';
LESSEQUAL: '<=';
GREATER: '>';
GREATEREQUAL: '>=';
andThen: AND THEN;
orElse: OR ELSE;
body: compoundStatement;

// builtInExp:
// 	getIntExp
// 	| putIntExp
// 	| putIntLnExp
// 	| getFloatExp
// 	| putFloatExp
// 	| putFloatLnExp
// 	| putBoolExp
// 	| putBoolLnExp
// 	| putStringExp
// 	| putStringLnExp
// 	| putLnExp;
// builtInFunCall:
// 	getInt
// 	| putInt
// 	| putIntLn
// 	| getFloat
// 	| putFloat
// 	| putFloatLn
// 	| putBool
// 	| putBoolLn
// 	| putString
// 	| putStringLn
// 	| putLn;

boollit: TRUE | FALSE;
keyword:
	BREAK
	| CONTINUE
	| FOR
	| TO
	| DOWNTO
	| DO
	| IF
	| THEN
	| ELSE
	| RETURN
	| WHILE
	| BEGIN
	| END
	| FUNCTION
	| PROCEDURE
	| VAR
	| TRUE
	| FALSE
	| ARRAY
	| OF
	| REALTYPE
	| BOOLEAN
	| INTTYPE
	| STRINGTYPE
	| NOT
	| AND
	| OR
	| DIV
	| MOD;
//5 EXPRESSION
exp: exp ( andThen | orElse ) exp1 | exp1;
exp1:
	exp2 (
		EQUAL
		| NOTEQUAL
		| LESS
		| LESSEQUAL
		| GREATER
		| GREATEREQUAL
	) exp2
	| exp2;
exp2: exp2 (ADD | SUB | OR) exp3 | exp3;
exp3: exp3 (DIVISION | MUL | DIV | MOD | AND) exp4 | exp4;
exp4: (SUB | NOT) exp4 | exp5;
exp5: literal | ID | funcallExp | indexExpression | LB exp RB;
indexExpression: (ID | funcallExp) LS exp RS;

INTLIT: [0-9]+;
FLOATLIT:
	('0' .. '9')+ (('.' ('0' .. '9')+ (EXPONENT)?)? | EXPONENT);

PROGRAM: P R O G R A M;
INTTYPE: I N T E G E R;
REALTYPE: R E A L;
BOOLTYPE: B O O L E A N;
BOOLEAN: B O O L E A N;
STRINGTYPE: S T R I N G;
VOIDTYPE: V O I D;

VAR: V A R;
ARRAY: A R R A Y;
OF: O F;
//2 STRUCTURE Var declaration
varDeclar: VAR listVarDeclar;

listVarDeclar: singleVarDeclar listVarDeclar | singleVarDeclar;

singleVarDeclar: listVar COLON varType SEMI;
listVar: ID COMMA listVar | ID;
varType: singleVarType | arrayVarType;
singleVarType: INTTYPE | REALTYPE | BOOLTYPE | STRINGTYPE;
arrayVarType:
	ARRAY LS lower DOUBLEDOT upper RS OF singleVarType;
lower: '-'?INTLIT;
upper: '-'?INTLIT;

//Function declaration
funcType: singleFuncType | arrayVarType;
singleFuncType: singleVarType | VOIDTYPE;

FUNCTION: F U N C T I O N;
funcDeclar:
	FUNCTION ID LB listPara? RB COLON varType SEMI varDeclar? compoundStatement;

listPara: paraDeclar SEMI listPara | paraDeclar;
paraDeclar: listVar COLON varType;

//Procedure declaration
PROCEDURE: P R O C E D U R E;
procDeclar:
	PROCEDURE ID LB listPara? RB SEMI varDeclar? compoundStatement;


///Lexical

//COMMENT: '/*' ('/'*? COMMENT | ('/'* | '*'*) ~[/*])*? '*'*? '*/' -> skip;

TRUE: T R U E;
FALSE: F A L S E;
//3.5 Literals
literal: INTLIT | FLOATLIT | boollit | STRINGLIT;

fragment EXPONENT: ('e' | 'E') ('+' | '-')? ('0' ..'9')+;

//6 STATEMENT AND CONTROL FLOW

//Assignment

assignStatement: listVarToAssign exp SEMI;
listVarToAssign:
	varElement ASSIGN listVarToAssign
	| varElement ASSIGN;

IF: I F;
THEN: T H E N;
ELSE: E L S E;
//If statement
ifStatement:
	IF exp THEN bodyStmt (
		ELSE bodyStmt2
	)?;
bodyStmt: statement | compoundStatement;
bodyStmt2: bodyStmt;

WHILE: W H I L E;
DO: D O;
//While statement
whileStatement: WHILE exp DO bodyStmt;

FOR: F O R;
TO: T O;
DOWNTO: D O W N T O;
//For statement
forStatement: FOR ID ASSIGN exp (TO | DOWNTO) expr2 DO bodyStmt;
expr2: exp;

BREAK: B R E A K;
//Break Statement
breakStatement: BREAK SEMI;

CONTINUE: C O N T I N U E;
//Continue Statement
continueStatement: CONTINUE SEMI;

RETURN: R E T U R N;
//Return Statement
returnStatement: RETURN exp? SEMI;

WITH: W I T H;
//With Statement
withStatement:
	WITH listVarDeclar DO bodyStmt;

BEGIN: B E G I N;
END: E N D;
//Compound Function
compoundStatement: BEGIN statement* END;
//Call Statement
funcallExp: ID LB listExp? RB;
//need to update in ast
listExp: exp COMMA listExp | exp;
callStatement: ID LB listExp? RB SEMI;

statement: (
		assignStatement
		| ifStatement
		| whileStatement
		| forStatement
		| withStatement
		| callStatement
		| breakStatement
		| continueStatement
		| returnStatement
	);

//Built-in Functions 
// GETINT: G E T I N T;
// PUTINT: P U T I N T;
// PUTINTLN: P U T I N T L N;
// GETFLOAT: G E T F L O A T;
// PUTFLOAT: P U T F L O A T;
// PUTFLOATLN: P U T F L O A T L N;
// PUTBOOL: P U T B O O L;
// PUTBOOLLN: P U T B O O L L N;
// PUTSTRING: P U T S T R I N G;
// PUTSTRINGLN: P U T S T R I N G L N;
// PUTLN: P U T L N;

varElement: ID | indexExpression;
// getIntExp: GETINT LB RB;
// putIntExp: PUTINT LB exp RB;
// putIntLnExp: PUTINTLN LB exp RB;
// getFloatExp: GETFLOAT LB RB;
// putFloatExp: PUTFLOAT LB exp RB;
// putFloatLnExp: PUTFLOATLN LB exp RB;
// putBoolExp: PUTBOOL LB exp RB;
// putBoolLnExp: PUTBOOLLN LB exp RB;
// putStringExp: PUTSTRING LB exp RB;
// putStringLnExp: PUTSTRINGLN LB exp RB;
// putLnExp: PUTLN LB RB;

// getInt: GETINT LB RB;
// putInt: PUTINT LB exp RB;
// putIntLn: PUTINTLN LB exp RB;
// getFloat: GETFLOAT LB RB;
// putFloat: PUTFLOAT LB exp RB;
// putFloatLn: PUTFLOATLN LB exp RB;
// putBool: PUTBOOL LB exp RB;
// putBoolLn: PUTBOOLLN LB exp RB;
// putString: PUTSTRING LB exp RB;
// putStringLn: PUTSTRINGLN LB exp RB;
// putLn: PUTLN LB RB;



ID: [a-zA-Z_][0-9a-zA-Z_]*;
STRINGLIT: DQ ( '\\' [btnfr"'\\] | ~[\b\t\f\r\n\\"] )* DQ {self.text = self.text.replace('"','');};
DQ: '"';
// STRINGLIT
// 	:    '"' ( '\\' [bfrnt"'\\] | ~[\b\n\t\f\r'\\"])* '"' ;
// STRINGLIT:
// 	'"' ~('\r' | '\n' | '"' | '\t' | '\\' | '\b' | '\f' | '\'')* '"';
fragment A: ('a' | 'A');
fragment B: ('b' | 'B');
fragment C: ('c' | 'C');
fragment D: ('d' | 'D');
fragment E: ('e' | 'E');
fragment F: ('f' | 'F');
fragment G: ('g' | 'G');
fragment H: ('h' | 'H');
fragment I: ('i' | 'I');
fragment J: ('j' | 'J');
fragment K: ('k' | 'K');
fragment L: ('l' | 'L');
fragment M: ('m' | 'M');
fragment N: ('n' | 'N');
fragment O: ('o' | 'O');
fragment P: ('p' | 'P');
fragment Q: ('q' | 'Q');
fragment R: ('r' | 'R');
fragment S: ('s' | 'S');
fragment T: ('t' | 'T');
fragment U: ('u' | 'U');
fragment V: ('v' | 'V');
fragment W: ('w' | 'W');
fragment X: ('x' | 'X');
fragment Y: ('y' | 'Y');
fragment Z: ('z' | 'Z');

ERROR_CHAR: .;
UNCLOSE_STRING: .;
ILLEGAL_ESCAPE: .;