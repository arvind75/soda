from rpython.jit.codewriter.policy import JitPolicy
from soda.interpreter import interpret
from soda.parser import parser
from soda.bytecode import compile_ast
from soda.fetcher import fetcher
import sys


def main(argv):
    isdump = False
    norun = False
    sourcefound = False
    for arg in argv:
        if arg.startswith("-"):
            if arg == "--dump":
                isdump = True
            elif arg == "--norun":
                norun = True
        elif arg.endswith(".na"):
            if not sourcefound:
                sourcefound = True
                root = arg.rstrip(".na")
                fetcher.packages.append(root)
    if sourcefound:
        bc = compile_ast(parser.parse(fetcher.gettokens()))
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
