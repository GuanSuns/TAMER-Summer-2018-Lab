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
FAST_EXPERIMENT = False      # no wait at the end of each epoch and no graphic output
TAMER_SHOW_LEARNED_VALUES = True   # whether to hide the learned Q-Values while learning
AUTO_FEEDBACK_TAMER = True     # use robot to simulate human feedback
#######################################################
############### VDBE values recorder ##################
#######################################################


class ExperimentConfigurator:
    experimentConfig = {'OUTPUT_DETAIL_LEVEL': VERY_SHORT_OUTPUT
        , 'text_only': False
        , 'display_speed': 0.5}

    gridworldConfig = {'grid_name': 'DiscountGrid'
        , 'discount': 0.9
        , 'noise': 0
        , 'grid_size': 150
        , 'n_episodes': 100
        , 'check_policy_converge': True
        , 'living_reward': 0}

    TamerConfig = {'is_asyn_input': True}

    qLearningConfig = {'learning_rate': 0.5
        , 'init_temp': 1.0
        , 'temp_decrease_rate': 1.0
        , 'epsilon': 0.3}

    def __init__():
        pass
