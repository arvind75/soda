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
        ":=",
        "=",
        "(",
        ")",
        "==",
        "!=",
        "<=",
        ">=",
        "<",
        ">",
        "&",
        "|",
        "!",
        ",",
        "NEG",
        "END",
        "NUMBER",
        "STRING",
        "IDENTIFIER",
        "PUT"
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


@pg.production("main : statementlist")
def main_block(s):
    return s[0]


@pg.production("statementlist : statementlist statement")
def statement_statement(s):
    s[0].append(s[1])
    return s[0]


@pg.production("statementlist : statement")
def statementlist_statement(s):
    return ast.List(s[0])


@pg.production("statement : PUT expression END")
def statement_put(s):
    sourcepos = s[0].getsourcepos()
    package = fetcher.packages[sourcepos.idx]
    line = str(sourcepos.lineno)
    col = str(sourcepos.colno)
    return ast.PutStatement(s[1], package, line, col)


@pg.production("statement : function")
def statement_function(s):
    return s[0]


@pg.production("statement : identifierlist := expressionlist END")
def statement_assignment(s):
    sourcepos = s[1].getsourcepos()
    package = fetcher.packages[sourcepos.idx]
    line = str(sourcepos.lineno)
    col = str(sourcepos.colno)
    return ast.Assignment(s[0], s[2], package, line, col)


# TODO: functions with no body, return only
@pg.production("returnstatement : expression END")
def returnstatement(s):
    return ast.ReturnStatement(s[0], "", "", "")


@pg.production("function : IDENTIFIER = statementlist returnstatement")
def function_noarg(s):
    sourcepos = s[1].getsourcepos()
    package = fetcher.packages[sourcepos.idx]
    line = str(sourcepos.lineno)
    col = str(sourcepos.colno)
    return ast.Function(s[0], [], s[2],
                        s[3], package, line, col)


@pg.production("function : IDENTIFIER paramlist = statementlist "
               "returnstatement")
def function_arg(s):
    sourcepos = s[2].getsourcepos()
    package = fetcher.packages[sourcepos.idx]
    line = str(sourcepos.lineno)
    col = str(sourcepos.colno)
    return ast.Function(s[0], s[1].get(), s[3],
                        s[4], package, line, col)


@pg.production("paramlist : paramlist IDENTIFIER")
def paramlist_paramlist(s):
    string = s[1].getstr()
    iden, trash = str_decode_utf_8(string, len(string), "strict", True)
    s[0].append(iden)
    return s[0]


@pg.production("paramlist : IDENTIFIER")
def paramlist_identifier(s):
    string = s[0].getstr()
    iden, trash = str_decode_utf_8(string, len(string), "strict", True)
    return ast.List(iden)


@pg.production("expressionlist : expressionlist , expressionlist")
def expressionlist_expressionlist(s):
    return ast.ExpressionPair(s[0], s[2])


@pg.production("expressionlist : expression")
def expressionlist_expression(s):
    return s[0]


@pg.production("identifierlist : identifierlist , identifierlist")
def identifierlist_identifierlist(s):
    return ast.IdentifierPair(s[0], s[2])


@pg.production("identifierlist : IDENTIFIER")
def identifierlist_identifier(s):
    string = s[0].getstr()
    iden, trash = str_decode_utf_8(string, len(string), "strict", True)
    return ast.RegisterVariable(iden)


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


@pg.production("expression : IDENTIFIER")
def expression_iden(s):
    sourcepos = s[0].getsourcepos()
    package = fetcher.packages[sourcepos.idx]
    line = str(sourcepos.lineno)
    col = str(sourcepos.colno)
    string = s[0].getstr()
    iden, trash = str_decode_utf_8(string, len(string), "strict", True)
    return ast.Variable(iden, package, line, col)


@pg.production("expression : STRING")
def expression_stringliteral(s):
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
    if token.name == "ERROR":
        sodaError(package, line, col, token.value)
    else:
        msg = "unexpected \"%s\"" % token.value
        sodaError(package, line, col, msg)


parser = pg.build()
