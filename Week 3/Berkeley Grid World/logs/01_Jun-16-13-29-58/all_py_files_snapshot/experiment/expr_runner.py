from experiment_creater_and_resumer.experiment_creater_and_resumer import ExprCreaterAndResumer


def run_expr():
    log_dir = '/Users/lguan/Documents/Study/Research/Summer 2018/Week 3/Berkeley Grid World/logs'
    expr_saver = ExprCreaterAndResumer(rootdir=log_dir)

    print('test logger -- %s' % __file__)
    expr_saver.dump_src_code_and_model_def(fname=__file__)


if __name__ == '__main__':
    run_expr()
