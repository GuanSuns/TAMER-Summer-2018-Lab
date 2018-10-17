# expr_launcher.py
#
# experiment launcher used in terminal (command line)
# -----------------------
import os
import sys
import time
import expr_configurator
from expr_configurator import ExperimentConfigurator
from environment import FirstOpenAIGym
from input import user_input
from experiment_saver.experiment_creater_and_resumer import ExprCreaterAndResumer


def run_expr():
    # configure the experiments
    config_experiment()
    # save experiment configurations
    save_experiment_info()

    expr_log_dir = ExperimentConfigurator.getExperimentConfig('root_log_dir')

    # run experiments

    raw_input('Press Enter to terminate the experiment')


def save_experiment_info():
    """
        Save the experiment configuration
        Must be called after config_experiment
        Must be called before generating any logging information
    """
    # generate postfix
    subject_name = ExperimentConfigurator.getExperimentConfig('subject_name')
    game_name = ExperimentConfigurator.getExperimentConfig('game')
    expr_date = ExperimentConfigurator.getExperimentConfig('date')
    postfix = subject_name + '_' + game_name + '_' + expr_date

    # create experiment log directory
    root_log_dir = ExperimentConfigurator.getExperimentConfig('root_log_dir')
    expr_saver = ExprCreaterAndResumer(rootdir=root_log_dir, postfix=postfix)
    expr_log_dir = expr_saver.getLogDir()
    ExperimentConfigurator.setExperimentConfig({'expr_log_dir': expr_log_dir})
    # extract the experiment identifier
    print(expr_log_dir)
    experiment_identifier = ''

    # save experiment launcher and expr_configurator
    expr_saver.dump_src_code_and_model_def(fname=__file__)
    # save experiment environment related files
    fname = FirstOpenAIGym.__file__
    if fname.endswith('.pyc'):
        fname = fname.replace(".pyc", ".py")
    expr_saver.dump_src_code_and_model_def(fname=fname)
    # save input module related files
    fname = user_input.__file__
    if fname.endswith('.pyc'):
        fname = fname.replace(".pyc", ".py")
    expr_saver.dump_src_code_and_model_def(fname=fname)

    # save the experiment configuration as json file
    config_fname = expr_log_dir + '/experiment_config.json'
    ExperimentConfigurator.saveConfigToFile(config_fname)


def config_experiment():
    # check if there are 3 user specified argument (not including the name of the python file)
    if len(sys.argv) != 4:
        print("Not enough arguments (need 3 but " + str(len(sys.argv) - 1) + ')')
        exit(1)

    # read the subject name
    subject_name = sys.argv[1]
    ExperimentConfigurator.setExperimentConfig({'subject_name': subject_name})

    # read the game name
    game_name = sys.argv[2]
    ExperimentConfigurator.setExperimentConfig({'game': game_name})

    # read root log directory
    root_log_dir = sys.argv[3]
    ExperimentConfigurator.setExperimentConfig({'root_log_dir': root_log_dir})

    # get current time
    str_time = time.strftime("%y%m%d%H%M")
    ExperimentConfigurator.setExperimentConfig({'date': str_time})


if __name__ == '__main__':
    run_expr()


