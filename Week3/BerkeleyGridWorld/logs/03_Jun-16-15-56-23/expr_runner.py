from experiment_creater_and_resumer.experiment_creater_and_resumer import ExprCreaterAndResumer
import gridworld


def run_expr():
    log_dir = '/Users/lguan/Documents/Study/Research/Summer 2018/Week 3/BerkeleyGridWorld/logs'
    expr_saver = ExprCreaterAndResumer(rootdir=log_dir)

    print('test logger -- %s' % __file__)
    expr_saver.dump_src_code_and_model_def(fname=__file__)

    tamerGridWorld = gridworld.TamerGridWorldExperiment()
    print(gridworld.__file__)
    expr_saver.dump_src_code_and_model_def(fname=gridworld.__file__)

    tamerGridWorld.run_episodes()


if __name__ == '__main__':
    run_expr()
