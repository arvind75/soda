# Phillip Wells
# CSCI-200 Algorithm Analysis

# target.py defines the entry point for translation
# and parses command-line arguments

from rpython.jit.codewriter.policy import JitPolicy
from rpython.rlib.streamio import open_file_as_stream
from soda.interpreter import interpret
from soda.parser import parser
from soda.bytecode import compile_ast
from soda.fetcher import fetcher
import os
import sys


def main(argv):
    isdump = False
    norun = False
    sourcefound = False
    extrafiles = []
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
                root = os.getcwd() + "/" + root
                fetcher.addpackage(root)
        else:
            extrafiles.append(arg)
    del extrafiles[0]
    if sourcefound:
        bc = compile_ast(parser.parse(fetcher.gettokens()))
        if isdump:
            print(bc.dump())
        if not norun:
            if extrafiles == []:
                bc.create_arrays("")
                interpret(bc)
            else:
                for filepath in extrafiles:
                    try:
                        sourcefile = open_file_as_stream(filepath)
                        data = sourcefile.readall()
                        sourcefile.close()
                        bc.create_arrays(data)
                        interpret(bc)
                    except OSError:
                        print("file %s not found" % filepath)
                        os._exit(-1)
    return 0


def jitpolicy(driver):
    return JitPolicy()


def target(driver, args):
    driver.exe_name = "csoda"
    return main, None


if __name__ == "__main__":
    main(sys.argv)
