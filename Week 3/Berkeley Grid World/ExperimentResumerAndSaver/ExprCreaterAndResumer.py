import shutil
import os
import time
import re
import sys


class ExprCreaterAndResumer:
    def __init__(self, rootdir, postfix=None):
        if not os.path.exists(rootdir):
            os.makedirs(rootdir)
        expr_dirs = os.listdir(rootdir)
        re_matches = [re.match("(\d+)_", x) for x in expr_dirs]
        expr_num = [int(x.group(1)) for x in re_matches if x is not None]
        highest_idx = np.argmax(expr_num) if len(expr_num)>0 else -1