from experiment_creater_and_resumer import experiment_creater_and_resumer
import gridworld
from input import user_input


def run_expr():
    log_dir = '/Users/lguan/Documents/Study/Research/Summer 2018/Week 3/BerkeleyGridWorld/logs'
    expr_saver = experiment_creater_and_resumer.ExprCreaterAndResumer(rootdir=log_dir)

    print('test logger -- %s' % __file__)
    expr_saver.dump_src_code_and_model_def(fname=__file__)

    tamerGridWorld = gridworld.TamerGridWorldExperiment()
    print(gridworld.__file__)
    # save grid world related files
    expr_saver.dump_src_code_and_model_def(fname=gridworld.__file__)
    # save input module related files
    expr_saver.dump_src_code_and_model_def(fname=user_input.__file__)

    tamerGridWorld.run_episodes()


if __name__ == '__main__':
    run_expr()
