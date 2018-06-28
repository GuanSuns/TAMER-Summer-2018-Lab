# expr_runner_ide.py
#
# experiment launcher for value iteration used in IDE
# -----------------------

from ..experiment_creater_and_resumer.experiment_creater_and_resumer import ExprCreaterAndResumer
from .. import gridworldValueIteration


def run_expr():
    # agent parameters
    alpha = 0.2     # learning rate
    epsilon = 0.3   # exploration rate

    # learning environment parameters
    display_speed = 0.5
    discount = 0.9
    delta = 0.02

    # generate postfix
    postfix = ''
    postfix += '_valueIteration'
    postfix += '_alpha' + str(alpha)
    postfix += '_epsilon' + str(epsilon)
    postfix += '_speed' + str(display_speed)

    log_dir = '/Users/lguan/Documents/Study/Research/Summer 2018/experiment-logs'
    expr_saver = ExprCreaterAndResumer(rootdir=log_dir, postfix=postfix)

    # save experiment runner
    expr_saver.dump_src_code_and_model_def(fname=__file__)
    # save grid world related files
    expr_saver.dump_src_code_and_model_def(fname=gridworldValueIteration.__file__)

    # run experiment
    exprValueIteration = gridworldValueIteration.GridworldValueIterationExperiment(learning_rate=alpha, epsilon=epsilon
                                                                                   , discount=discount, delta=delta
                                                                                   , display_speed=display_speed)
    exprValueIteration.start()


if __name__ == '__main__':
    run_expr()
