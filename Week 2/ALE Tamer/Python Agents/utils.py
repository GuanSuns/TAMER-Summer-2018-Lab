# util.py
#
# Some utility functions for python agents
# -------

import sys


def raiseNotDefined(method_name):
    print("Method not implemented: %s" % method_name)
    sys.exit(1)
