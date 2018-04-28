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
        "[",
        "]",
        "==",
        "!=",
        "<=",
        ">=",
        "<",
        ">",
        "&",
        "|",
        "!",
        ".",
        ",",
        ";",
        ":",
        "NEG",
        "END",
        "NUMBER",
        "STRING",
        "FN",
        "IF",
        "THEN",
        "ELSE",
        "FOR",
        "ENDLOOP",
        "BREAK",
        "WHERE",
        "LEN",
        "IN",
        "CHARS",
        "WORDS",
        "LINES",
        "IDENTIFIER"
    ],
    precedence=[
        ("left", ["|"]),
        ("left", ["&"]),
        ("left", ["==", "!=", "<=", ">=", "<", ">"]),
        ("left", ["+", "-", "++", "--"]),
        ("left", ["*", "/", "%"]),
        ("left", ["^"]),
        ("left", ["NEG", "!", "["])
    ],
    cache_id="soda",
)


@pg.production("main : statementlist")
def main_statementlist(s):
    return s[0]


@pg.production("statementlist : statementlist statement")
def statementlist_statementlist(s):
    s[0].append(s[1])
    return s[0]


@pg.production("statementlist : statement")
def statementlist_statement(s):
    return ast.List(s[0])


@pg.production("statement : function END")
def statement_function(s):
    return s[0]


@pg.production("statement : expression END")
def statement_expression(s):
    return ast.Expression(s[0])


@pg.production("statement : BREAK END")
def statement_break(s):
    sourcepos = s[0].getsourcepos()
    package = fetcher.packages[sourcepos.idx]
    line = str(sourcepos.lineno)
    col = str(sourcepos.colno)
    return ast.Break(package, line, col)


@pg.production("statement : IF expression END THEN statementlist "
               "ELSE statement")
def statement_if(s):
    sourcepos = s[0].getsourcepos()
    package = fetcher.packages[sourcepos.idx]
    line = str(sourcepos.lineno)
    col = str(sourcepos.colno)
    return ast.If(s[1], s[4].get(), s[6], package, line, col)


@pg.production("statement : FOR smlstatement ; expression ; smlstatement END"
               " statementlist ENDLOOP END")
def statement_for(s):
    sourcepos = s[0].getsourcepos()
    package = fetcher.packages[sourcepos.idx]
    line = str(sourcepos.lineno)
    col = str(sourcepos.colno)
    return ast.For(s[1], s[3], s[5], s[7].get(),
                   package, line, col)


@pg.production("statement : FOR expression END statementlist ENDLOOP END")
def statement_while(s):
    sourcepos = s[0].getsourcepos()
    package = fetcher.packages[sourcepos.idx]
    line = str(sourcepos.lineno)
    col = str(sourcepos.colno)
    return ast.While(s[1], s[3].get(), package, line, col)


@pg.production("statement : FOR IDENTIFIER IN expression END "
               "statementlist ENDLOOP END")
def statement_iterate(s):
    sourcepos = s[0].getsourcepos()
    package = fetcher.packages[sourcepos.idx]
    line = str(sourcepos.lineno)
    col = str(sourcepos.colno)
    return ast.Iterate(s[1], s[3], s[5].get(), package, line, col)


@pg.production("smlstatement : expression")
def smlstatement_expression(s):
    return s[0]


@pg.production("smlstatement : identifierlist := expressionlist")
def smlstatement_assignment(s):
    sourcepos = s[1].getsourcepos()
    package = fetcher.packages[sourcepos.idx]
    line = str(sourcepos.lineno)
    col = str(sourcepos.colno)
    if not len(s[0].get()) == len(s[2].get()):
        sodaError(package, line, col, "assignment operator requires number "
                  "of variables to match number of expressions")
    return ast.Assignment(s[0], s[2], package, line, col)


@pg.production("statement : identifierlist := expressionlist END")
def statement_assignment(s):
    sourcepos = s[1].getsourcepos()
    package = fetcher.packages[sourcepos.idx]
    line = str(sourcepos.lineno)
    col = str(sourcepos.colno)
    if not len(s[0].get()) == len(s[2].get()):
        sodaError(package, line, col, "assignment operator requires number "
                  "of variables to match number of expressions")
    return ast.Assignment(s[0], s[2], package, line, col)


@pg.production("returnstatement : expression")
def returnstatement(s):
    return ast.ReturnStatement(s[0], "", "", "")


@pg.production("function : FN IDENTIFIER ( ) = returnstatement WHERE "
               "statementlist ENDLOOP")
def function_noarg(s):
    sourcepos = s[0].getsourcepos()
    package = fetcher.packages[sourcepos.idx]
    line = str(sourcepos.lineno)
    col = str(sourcepos.colno)
    return ast.Function(s[1], [], s[7].get(),
                        s[5], package, line, col)


@pg.production("function : FN IDENTIFIER ( ) = returnstatement")
def function_nostatement_noarg(s):
    sourcepos = s[0].getsourcepos()
    package = fetcher.packages[sourcepos.idx]
    line = str(sourcepos.lineno)
    col = str(sourcepos.colno)
    return ast.Function(s[1], [], [],
                        s[5], package, line, col)


@pg.production("function : FN IDENTIFIER ( paramlist ) = returnstatement")
def function_nostatement_arg(s):
    sourcepos = s[0].getsourcepos()
    package = fetcher.packages[sourcepos.idx]
    line = str(sourcepos.lineno)
    col = str(sourcepos.colno)
    return ast.Function(s[1], s[3].get(), [],
                        s[6], package, line, col)


@pg.production("function : FN IDENTIFIER ( paramlist ) = returnstatement "
               "WHERE statementlist ENDLOOP")
def function_arg(s):
    sourcepos = s[0].getsourcepos()
    package = fetcher.packages[sourcepos.idx]
    line = str(sourcepos.lineno)
    col = str(sourcepos.colno)
    return ast.Function(s[1], s[3].get(), s[8].get(),
                        s[6], package, line, col)


@pg.production("paramlist : paramlist , identifier")
def paramlist_paramlist(s):
    s[0].append(s[2])
    return s[0]


@pg.production("paramlist : identifier")
def paramlist_identifier(s):
    return ast.List(s[0])


@pg.production("itemslist : itemslist , pair")
def itemslist_itemslist(s):
    for item in s[2].get():
        s[0].append(item)
    return s[0]


@pg.production("itemslist : pair")
def itemslist_pair(s):
    return s[0]


@pg.production("pair : expression : expression END")
@pg.production("pair : expression : expression")
def pair(s):
    lst = ast.List(s[0])
    lst.append(s[2])
    return lst


@pg.production("expressionlist : expressionlist , expression")
def expressionlist_expressionlist(s):
    s[0].append(s[2])
    return s[0]


@pg.production("expressionlist : expression")
def expressionlist_expression(s):
    return ast.List(s[0])


@pg.production("identifierlist : identifierlist , identifier")
def identifierlist_identifierlist(s):
    s[0].append(s[2])
    return s[0]


@pg.production("identifierlist : identifier")
def identifierlist_identifier(s):
    return ast.List(s[0])


@pg.production("identifier : IDENTIFIER")
def identifier(s):
    sourcepos = s[0].getsourcepos()
    package = fetcher.packages[sourcepos.idx]
    line = str(sourcepos.lineno)
    col = str(sourcepos.colno)
    return ast.RegisterVariable(s[0], package, line, col)


@pg.production("identifier : expression [ expression ]")
def identifier_index(s):
    sourcepos = s[1].getsourcepos()
    package = fetcher.packages[sourcepos.idx]
    line = str(sourcepos.lineno)
    col = str(sourcepos.colno)
    return ast.SetIndex(s[0], s[2], package, line, col)


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


@pg.production("expression : variable")
def expression_variable(s):
    return s[0]


@pg.production("variable : IDENTIFIER")
def variable_iden(s):
    sourcepos = s[0].getsourcepos()
    package = fetcher.packages[sourcepos.idx]
    line = str(sourcepos.lineno)
    col = str(sourcepos.colno)
    return ast.Variable(s[0], None, package, line, col)


@pg.production("variable : IDENTIFIER . IDENTIFIER")
def variable_qualifiediden(s):
    sourcepos = s[2].getsourcepos()
    package = fetcher.packages[sourcepos.idx]
    line = str(sourcepos.lineno)
    col = str(sourcepos.colno)
    return ast.Variable(s[2], s[0], package, line, col)


@pg.production("expression : IDENTIFIER ( expressionlist )")
def expression_call(s):
    sourcepos = s[0].getsourcepos()
    package = fetcher.packages[sourcepos.idx]
    line = str(sourcepos.lineno)
    col = str(sourcepos.colno)
    return ast.Call(s[0], None, s[2].get(), package, line, col)


@pg.production("expression : IDENTIFIER . IDENTIFIER ( expressionlist )")
def expression_qualifiedcall(s):
    sourcepos = s[2].getsourcepos()
    package = fetcher.packages[sourcepos.idx]
    line = str(sourcepos.lineno)
    col = str(sourcepos.colno)
    return ast.Call(s[2], s[0], s[4].get(), package, line, col)


@pg.production("expression : IDENTIFIER ( ) ")
def expression_call_noargs(s):
    sourcepos = s[0].getsourcepos()
    package = fetcher.packages[sourcepos.idx]
    line = str(sourcepos.lineno)
    col = str(sourcepos.colno)
    return ast.Call(s[0], None, [], package, line, col)


@pg.production("expression : IDENTIFIER . IDENTIFIER ( ) ")
def expression_qualifiedcall_noargs(s):
    sourcepos = s[2].getsourcepos()
    package = fetcher.packages[sourcepos.idx]
    line = str(sourcepos.lineno)
    col = str(sourcepos.colno)
    return ast.Call(s[2], s[0], [], package, line, col)


@pg.production("expression : number")
def expression_number(s):
    return s[0]


@pg.production("expression : LEN ( expression )")
def expression_len(s):
    sourcepos = s[0].getsourcepos()
    package = fetcher.packages[sourcepos.idx]
    line = str(sourcepos.lineno)
    col = str(sourcepos.colno)
    return ast.Len(s[2], package, line, col)


@pg.production("number : NUMBER")
def number_number(s):
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


@pg.production("expression : STRING")
def expression_stringliteral(s):
    sourcepos = s[0].getsourcepos()
    package = fetcher.packages[sourcepos.idx]
    line = str(sourcepos.lineno)
    col = str(sourcepos.colno)
    return ast.String(s[0], package, line, col)


@pg.production("expression : CHARS")
def expression_chars(s):
    sourcepos = s[0].getsourcepos()
    package = fetcher.packages[sourcepos.idx]
    line = str(sourcepos.lineno)
    col = str(sourcepos.colno)
    return ast.Chars(package, line, col)


@pg.production("expression : WORDS")
def expression_words(s):
    sourcepos = s[0].getsourcepos()
    package = fetcher.packages[sourcepos.idx]
    line = str(sourcepos.lineno)
    col = str(sourcepos.colno)
    return ast.Words(package, line, col)


@pg.production("expression : LINES")
def expression_lines(s):
    sourcepos = s[0].getsourcepos()
    package = fetcher.packages[sourcepos.idx]
    line = str(sourcepos.lineno)
    col = str(sourcepos.colno)
    return ast.Lines(package, line, col)


@pg.production("expression : expression [ expression ]")
def expression_index(s):
    sourcepos = s[1].getsourcepos()
    package = fetcher.packages[sourcepos.idx]
    line = str(sourcepos.lineno)
    col = str(sourcepos.colno)
    return ast.GetIndex(s[0], s[2], package, line, col)


@pg.production("expression : [ ]")
def expression_emptyarray(s):
    sourcepos = s[0].getsourcepos()
    package = fetcher.packages[sourcepos.idx]
    line = str(sourcepos.lineno)
    col = str(sourcepos.colno)
    return ast.Array([], package, line, col)


@pg.production("expression : [ itemslist ]")
def expression_array(s):
    sourcepos = s[0].getsourcepos()
    package = fetcher.packages[sourcepos.idx]
    line = str(sourcepos.lineno)
    col = str(sourcepos.colno)
    return ast.Array(s[1].reverse(), package, line, col)


@pg.production("expression : [ expressionlist END ]")
@pg.production("expression : [ expressionlist ]")
def expression_normalizedarray(s):
    sourcepos = s[0].getsourcepos()
    package = fetcher.packages[sourcepos.idx]
    line = str(sourcepos.lineno)
    col = str(sourcepos.colno)
    lst = s[1].get()
    enumlist = []
    a = rbigint()
    for i in range(0, len(lst)):
        enumlist.append(ast.Integer(a.fromint(i),
                                    package, line, col))
        enumlist.append(lst[i])
    enumlist.reverse()
    return ast.Array(enumlist, package, line, col)


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
