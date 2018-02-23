import os

WINDOWS = "nt"
RED = "\033[91m"
NORMAL = "\033[0m"

def sodaError(message):
    if os.name == WINDOWS:
        os.write(2, "error: %s\n" % (message))
    else:
        os.write(2, "%s error: %s %s\n" % (RED, NORMAL, message))
    os._exit(1)

def lexError(package, line, col, msg):
    if os.name == WINDOWS:
        os.write(2, "%s.na:%s:%s: %s" % (package, line, col, msg))
    else:
        os.write(2, "%s%s.na:%s:%s:%s %s" % (RED, package, line, col, NORMAL, msg))
    os._exit(1)
