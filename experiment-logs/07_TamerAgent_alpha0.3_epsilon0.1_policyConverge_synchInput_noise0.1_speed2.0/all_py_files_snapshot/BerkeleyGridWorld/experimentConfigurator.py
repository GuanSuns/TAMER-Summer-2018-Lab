# experimentConfigurator.py
# ------------
# The central configurator for experiment.
# You can set the values for all related parameters here


#######################################################
######## Output detail level control ##################
#######################################################
VERY_SHORT_OUTPUT = 0
SHORT_OUTPUT = 1
SOME_DETAILS = 2
#######################################################


class ExperimentConfigurator:
    experimentConfig = {'OUTPUT_DETAIL_LEVEL': VERY_SHORT_OUTPUT
        , 'check_policy_converge': True
        , 'text_only': False
        , 'agent_type': 'qLearningAgent'
        , 'Fast_Experiment': False      # no wait at the end of each epoch and no graphic output
        , 'display_speed': 0.5}

    gridworldConfig = {'grid_name': 'DiscountGrid'
        , 'discount': 0.9
        , 'noise': 0
        , 'grid_size': 150
        , 'n_episodes': 100
        , 'living_reward': 0}

    TamerConfig = {'is_asyn_input': True
        , 'agent_max_n_experiences': 1000
        , 'agent_window_size': 1.0
        , 'Auto_Feedback_TAMER': True
        , 'TAMER_Show_Learned_Values': True}    # whether to hide the learned Q-Values while learning

    qLearningConfig = {'learning_rate': 0.5
        , 'init_temp': 1.0
        , 'use_VDBE': False
        , 'temp_decrease_rate': 1.0
        , 'epsilon': 0.3}

    @staticmethod
    def getOutputDetailLevel():
        return ExperimentConfigurator.experimentConfig['OUTPUT_DETAIL_LEVEL']

    def __init__():
        pass
