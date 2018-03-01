from rpython.rlib.runicode import str_decode_utf_8
from rpython.rlib.rbigint import rbigint
from rply import ParserGenerator
from soda.errors import sodaError
from soda.fetch import fetcher
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
        "ERROR"
    ],
    precedence=[
        ("left", ["+", "-"]),
        ("left", ["*", "/", "%"]),
        ("left", ["^"])
    ],
    cache_id="soda",
)


@pg.production("main : statement")
def main_block(s):
    return s[0]


@pg.production("statement : statement statement")
def statement_statement(s):
    return ast.StatementPair(s[0], s[1])


@pg.production("statement : PRINTLN expression")
def println_expression(s):
    return ast.PrintlnStatement(s[1])


@pg.production("expression : expression  +  expression")
@pg.production("expression : expression  -  expression")
@pg.production("expression : expression  *  expression")
@pg.production("expression : expression  /  expression")
@pg.production("expression : expression  %  expression")
@pg.production("expression : expression  ^  expression")
def expression_binop(s):
    return ast.BinOp(s[1].getstr(), s[0], s[2])


@pg.production("expression : ( expression )")
def expression_paren(s):
    return s[1]


@pg.production("expression : NUMBER")
def expression_number(s):
    a = rbigint()
    return ast.Number(a.fromstr(s[0].getstr()))


@pg.production("expression : stringliteral")
def expression_stringliteral(s):
    return s[0]


@pg.production("stringliteral : STRING")
def stringliteral_string(s):
    string = s[0].getstr()
    string, trash = str_decode_utf_8(string, len(string), "strict", True)
    return ast.String(string)


@pg.error
def error_handler(token):
    package = fetcher.packages[token.getsourcepos().idx]
    line = str(token.getsourcepos().lineno)
    col = str(token.getsourcepos().colno)
    if token.value == "$end":
        sodaError(package, line, col, "EOF error")
    elif token.name == "ERROR":
        sodaError(package, line, col, token.value)
    else:
        msg = "unexpected %s" % token.value
        sodaError(package, line, col, msg)


parser = pg.build()
