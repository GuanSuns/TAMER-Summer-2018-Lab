# expr_runner_terminal.py
#
# experiment launcher used in terminal (command line)
# -----------------------

from ..experiment_creater_and_resumer.experiment_creater_and_resumer import ExprCreaterAndResumer
from .. import gridworld
from ..input import user_input


def run_expr():
    # agent parameters
    is_use_q_agent = True  # use qAgent or use Tamer agent
    alpha = 0.2     # learning rate
    epsilon = 0.3   # exploration rate
    window_size = 1     # Tamer agent window size
    max_n_experience = 1000     # Tamer agent maximum number of experiences

    # learning environment parameters
    n_episodes = 100
    display_speed = 0.5

    # generate postfix
    postfix = ''
    postfix += 'agent' + ('Q' if is_use_q_agent else 'Tamer')
    postfix += '_alpha' + str(alpha)
    postfix += '_epsilon' + str(epsilon)
    postfix += '_winSize' + str(window_size)
    postfix += '_speed' + str(display_speed)

    log_dir = '/Users/lguan/Documents/Study/Research/Summer 2018/Week3/BerkeleyGridWorld/logs'
    expr_saver = ExprCreaterAndResumer(rootdir=log_dir, postfix=postfix)

    # save experiment runner
    expr_saver.dump_src_code_and_model_def(fname=__file__)
    # save grid world related files
    expr_saver.dump_src_code_and_model_def(fname=gridworld.__file__)
    # save input module related files
    expr_saver.dump_src_code_and_model_def(fname=user_input.__file__)

    # run experiment
    tamerGridWorld = gridworld.TamerGridWorldExperiment(learning_rate=alpha, epsilon=epsilon
                                                        , agent_max_n_experiences=max_n_experience
                                                        , agent_window_size=window_size
                                                        , n_episodes=n_episodes
                                                        , display_speed=display_speed
                                                        , is_use_q_agent=is_use_q_agent)
    tamerGridWorld.run_episodes()


if __name__ == '__main__':
    run_expr()
