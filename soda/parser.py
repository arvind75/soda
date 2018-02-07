from rpython.rlib.runicode import str_decode_utf_8
from rply import ParserGenerator
from soda.stringfmt import
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
        "PRINT",
    ],
    precedence=[
        ("left", ["+", "-"]),
        ("left", ["*", "/", "%"]),
        ("left", ["^"])
    ],
    cache_id="soda",
)

@pg.production("main : statement")
def main_program(s):
    return s[0]

@pg.production("statement : statement statement")
def statement_statement(s):
    return ast.Pair(s[0], s[1])

@pg.production("statement : expression")
def statement_expression(s):
    return ast.Statement(s[0])

@pg.production("statement : PRINT expression")
def print_expression(s):
    return ast.PrintStatement(s[1])

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

@pg.production("expression : STRING")
def expression_string(s):
    string = s[0].getstr()
    string = string[:-1]
    string = string[1:]
    string, trash = str_decode_utf_8(string, len(string), "strict", True)
    return ast.String(string)

parser = pg.build()
