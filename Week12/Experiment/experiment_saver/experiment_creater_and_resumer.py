import shutil
import os
import time
import re
import sys
import numpy as np


class ExprCreaterAndResumer:
    def __init__(self, rootdir, postfix=None):
        if not os.path.exists(rootdir):
            os.makedirs(rootdir)
        expr_dirs = os.listdir(rootdir)
        re_matches = [re.match("(\d+)_", x) for x in expr_dirs]
        expr_num = [int(x.group(1)) for x in re_matches if x is not None]
        highest_idx = np.argmax(expr_num) if len(expr_num) > 0 else -1

        # dir name is like "5_Mar-09-12-27-59" or "5_<postfix>"
        self.dir = rootdir + '/' + '%02d' % (expr_num[highest_idx] + 1 if highest_idx != -1 else 0) + \
                   '_' + (postfix if postfix else time.strftime("%b-%d-%H-%M-%S"))
        os.makedirs(self.dir)
        self.logfile = open(self.dir + "/log.txt", 'a')  # no buffer
        self.redirect_output_to_logfile_as_well()

    def getLogDir(self):
        return self.dir

    def redirect_output_to_logfile_as_well(self):
        class Logger(object):
            def __init__(self, logfile):
                self.stdout = sys.stdout
                self.logfile = logfile

            def write(self, message):
                self.stdout.write(message)
                self.logfile.write(message)

            def flush(self):
                # this flush method is needed for python 3 compatibility.
                # this handles the flush command by doing nothing.
                # you might want to specify some extra behavior here.
                pass

        sys.stdout = Logger(self.logfile)
        sys.stderr = sys.stdout
        # Now you can use: `print "Hello"`, which will write "Hello" to both stdout and logfile

    def dump_src_code_and_model_def(self, fname):
        fname = os.path.abspath(fname)  # if already absolute path, it does nothing
        shutil.copyfile(fname, self.dir + '/' + os.path.basename(fname))

        # copy all py files in current directory
        task_dir = fname.split('/')[-2]  # this will give "gaze" "modeling" etc
        task_snapshot_dir = self.dir + '/all_py_files_snapshot/' + task_dir
        os.makedirs(task_snapshot_dir)
        task_py_files = [os.path.dirname(fname) + '/' + x for x in os.listdir(os.path.dirname(fname)) if
                         x.endswith('.py')]
        for py in task_py_files:
            shutil.copyfile(py, task_snapshot_dir + '/' + os.path.basename(py))
            if '__init__.py' in py:
                shutil.copyfile(py, self.dir + '/all_py_files_snapshot/' + os.path.basename(py))

