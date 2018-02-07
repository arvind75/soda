from rpython.rlib.streamio import open_file_as_stream
from rpython.jit.codewriter.policy import JitPolicy
from soda.interpreter import interpret
from soda.parser import parser
from soda.lexer import lexer
from soda.bytecode import compile_ast
import sys

def main(argv):
    isdump = False
    norun = False
    sourcefound = False
    data = ""
    for arg in argv:
        if arg.startswith("-"):
            if arg == "--dump":
                isdump = True
            elif arg == "--norun":
                norun = True
        elif arg.endswith(".na"):
            if not sourcefound:
                try:
                    f = open_file_as_stream(arg)
                    data = f.readall()
                    f.close()
                    sourcefound = True
                except Exception as e:
                    print("Fatal error: %s" % e)
                    return 1
        
    if not data == "":
        bc = compile_ast(parser.parse(lexer.lex(data)))
        if isdump:
            print(bc.dump())
        if not norun:
            interpret(bc)
        
    return 0

def jitpolicy(driver):
    return JitPolicy()

def target(driver, args):
    driver.exe_name = "csoda"
    return main, None

if __name__ == "__main__":
    main(sys.argv)
