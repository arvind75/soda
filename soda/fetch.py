from rpython.rlib.streamio import open_file_as_stream
import os
from lexer import lexer
from parser import parser
from bytecode import compile_ast

def compile_dependencies(path):
    filepath = os.getcwd() + "/" + path + ".na"
    data = []
    try:
        file = open_file_as_stream(filepath)
        data.append(file.readall())
        file.close()
        ast_node = "".join(data)
        compiled = compile_ast(parser.parse(lexer.lex(ast_node)))
        return compiled
    except OSError:
        print("fetch error: package %s not found" %path)
