# Phillip Wells
# CSCI-200 Algorithm Analysis

# error.py defines the sodaError() function

import os

WINDOWS = "nt"
RED = "\033[91m"
NORMAL = "\033[0m"


def sodaError(package, line, col, message):
    if os.name == WINDOWS:
        os.write(2, "%s.na:%s:%s: %s\n" % (package, line, col, message))
    else:
        os.write(2, "%s%s.na:%s:%s:%s %s\n" % (RED, package, line, col,
                                               NORMAL, message))
    os._exit(1)
