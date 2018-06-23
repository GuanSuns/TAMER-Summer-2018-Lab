# expr_runner_ide.py
#
# experiment launcher used in IDE like Pygame
# -----------------------

from experiment_creater_and_resumer.experiment_creater_and_resumer import ExprCreaterAndResumer
import gridworld
from input import user_input


def run_expr():
    log_dir = '/Users/lguan/Documents/Study/Research/Summer 2018/Week3/BerkeleyGridWorld/logs'
    expr_saver = ExprCreaterAndResumer(rootdir=log_dir)

    # save experiment runner
    expr_saver.dump_src_code_and_model_def(fname=__file__)
    # save grid world related files
    expr_saver.dump_src_code_and_model_def(fname=gridworld.__file__)
    # save input module related files
    expr_saver.dump_src_code_and_model_def(fname=user_input.__file__)

    # run experiment
    tamerGridWorld = gridworld.TamerGridWorldExperiment()
    tamerGridWorld.run_episodes()


if __name__ == '__main__':
    run_expr()
