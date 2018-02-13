from rpython.rlib.streamio import open_file_as_stream
from rpython.jit.codewriter.policy import JitPolicy
from soda.interpreter import interpret
from soda.parser import parser
from soda.bytecode import compile_ast
from soda.fetch import fetcher
import sys

def main(argv):
    isdump = False
    norun = False
    sourcefound = False
    data = []
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
                    data.append(f.readall())
                    f.close()
                    sourcefound = True
                    fetcher.add_package(arg.rstrip(".na"))
                except OSError as e:
                    print("Fatal error: %s" % e)
                    return 1
        
    if not data == []:
        data = "".join(data)
        strippedtokens = fetcher.find()
        tokenlist = []
        bc = compile_ast(parser.parse(strippedtokens))
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
