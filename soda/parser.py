from rpython.rlib.runicode import str_decode_utf_8
from rply import ParserGenerator
from soda.lexer import lexer
from soda import ast

pg = ParserGenerator(
    [
        "+",
        "-",
        "*",
        "/",
        "%",
        "^",
        "(",
        ")",
        "NUMBER",
        "STRING",
        "PRINTLN",
    ],
    precedence=[
        ("left", ["+", "-"]),
        ("left", ["*", "/", "%"]),
        ("left", ["^"])
    ],
    cache_id="soda",
)

@pg.production("main : statement")
def main_statement(s):
    return s[0]

@pg.production("statement : statement statement")
def statement_statement(s):
    return ast.StatementPair(s[0], s[1])

@pg.production("statement : expression")
def statement_expression(s):
    return ast.Statement(s[0])

@pg.production("statement : PRINTLN expression")
def println_expression(s):
    return ast.PrintlnStatement(s[1])

@pg.production("expression : expression + expression")
@pg.production("expression : expression - expression")
@pg.production("expression : expression * expression")
@pg.production("expression : expression / expression")
@pg.production("expression : expression % expression")
@pg.production("expression : expression ^ expression")
def expression_binop(s):
    return ast.BinOp(s[1].getstr(), s[0], s[2])

@pg.production("expression : ( expression )")
def expression_paren(s):
    return s[1]

@pg.production("expression : NUMBER")
def expression_number(s):
    return ast.Number(float(s[0].getstr()))

@pg.production("expression : stringliteral")
def expression_stringliteral(s):
    return s[0]

@pg.production("stringliteral : STRING")
def stringliteral_string(s):
    string = s[0].getstr()
    string = string[:-1]
    string = string[1:]
    string, trash = str_decode_utf_8(string, len(string), "strict", True)
    return ast.String(string)

parser = pg.build()
