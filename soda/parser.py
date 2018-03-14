from rpython.rlib.runicode import str_decode_utf_8
from rpython.rlib.rbigint import rbigint
from rply import ParserGenerator
from soda.errors import sodaError
from soda.fetcher import fetcher
from soda import ast

pg = ParserGenerator(
    [
        "+",
        "++",
        "-",
        "--",
        "*",
        "/",
        "%",
        "^",
        "(",
        ")",
        "=",
        "==",
        "!=",
        "<=",
        ">=",
        "<",
        ">",
        "&",
        "|",
        "!",
        "NEG",
        "END",
        "NUMBER",
        "STRING",
        "PUT",
        "ERROR"
    ],
    precedence=[
        ("left", ["|"]),
        ("left", ["&"]),
        ("left", ["==", "!=", "<=", ">=", "<", ">"]),
        ("left", ["+", "-", "++", "--"]),
        ("left", ["*", "/", "%"]),
        ("left", ["^"]),
        ("left", ["NEG", "!"])
    ],
    cache_id="soda",
)


@pg.production("main : statement")
def main_block(s):
    return s[0]


@pg.production("statement : statement statement")
def statement_statement(s):
    return ast.StatementPair(s[0], s[1])


@pg.production("statement : PUT expression END")
def put_expression(s):
    sourcepos = s[0].getsourcepos()
    package = fetcher.packages[sourcepos.idx]
    line = str(sourcepos.lineno)
    col = str(sourcepos.colno)
    return ast.PutStatement(s[1], package, line, col)


@pg.production("expression : expression  +  expression")
@pg.production("expression : expression  ++  expression")
@pg.production("expression : expression  --  expression")
@pg.production("expression : expression  -  expression")
@pg.production("expression : expression  *  expression")
@pg.production("expression : expression  /  expression")
@pg.production("expression : expression  %  expression")
@pg.production("expression : expression  ^  expression")
@pg.production("expression : expression  ==  expression")
@pg.production("expression : expression  !=  expression")
@pg.production("expression : expression  <=  expression")
@pg.production("expression : expression  >=  expression")
@pg.production("expression : expression  <  expression")
@pg.production("expression : expression  >  expression")
@pg.production("expression : expression  &  expression")
@pg.production("expression : expression  |  expression")
def expression_binop(s):
    sourcepos = s[1].getsourcepos()
    package = fetcher.packages[sourcepos.idx]
    line = str(sourcepos.lineno)
    col = str(sourcepos.colno)
    return ast.BinOp(s[1].getstr(), s[0], s[2],
                     package, line, col)


@pg.production("expression : ! expression")
@pg.production("expression : NEG expression")
def expression_unop(s):
    sourcepos = s[0].getsourcepos()
    package = fetcher.packages[sourcepos.idx]
    line = str(sourcepos.lineno)
    col = str(sourcepos.colno)
    return ast.UnOp(s[0].getstr(), s[1], package, line, col)


@pg.production("expression : ( expression )")
def expression_paren(s):
    return s[1]


@pg.production("expression : NUMBER")
def expression_number(s):
    sourcepos = s[0].getsourcepos()
    package = fetcher.packages[sourcepos.idx]
    line = str(sourcepos.lineno)
    col = str(sourcepos.colno)
    try:
        a = rbigint()
        return ast.Integer(a.fromstr(s[0].getstr()),
                           package, line, col)
    except Exception:
        package = fetcher.packages[s[0].getsourcepos().idx]
        line = str(s[0].getsourcepos().lineno)
        col = str(s[0].getsourcepos().colno)
        msg = "error in number %s" % s[0].getstr()
        sodaError(package, line, col, msg)


@pg.production("expression : stringliteral")
def expression_stringliteral(s):
    return s[0]


@pg.production("stringliteral : STRING")
def stringliteral_string(s):
    sourcepos = s[0].getsourcepos()
    package = fetcher.packages[sourcepos.idx]
    line = str(sourcepos.lineno)
    col = str(sourcepos.colno)
    string = s[0].getstr()
    string, trash = str_decode_utf_8(string, len(string), "strict", True)
    return ast.String(string, package, line, col)


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
