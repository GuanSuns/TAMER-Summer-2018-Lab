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
    experimentConfig = {
        'OUTPUT_DETAIL_LEVEL': VERY_SHORT_OUTPUT
        , 'check_policy_converge': True
        , 'text_only': False
        , 'agent_type': 'qLearningAgent'
        , 'Fast_Experiment': False      # no wait at the end of each epoch and no graphic output
        , 'save_VDBE': False
        , 'display_speed': 2.0}

    gridWorldConfig = {
        'grid_name': 'DiscountGrid'
        , 'discount': 0.9
        , 'noise': 0
        , 'grid_size': 150
        , 'n_episodes': 100
        , 'living_reward': 0}

    TamerConfig = {
        'is_asyn_input': False
        , 'agent_max_n_experiences': 1000
        , 'agent_window_size': 1.0
        , 'Auto_Feedback_TAMER': True
        , 'TAMER_Show_Learned_Values': True}    # whether to hide the learned Q-Values while learning

    qLearningConfig = {
        'learning_rate': 0.5
        , 'init_temp': 1.0
        , 'use_VDBE': False
        , 'temp_decrease_rate': 1.0
        , 'epsilon': 0.3}   # set epsilon to -1 to use softmax

    VDBEConfig = {
        'use_VDBE': False
        , 'sigma': 0.05
        , 'delta': 0.1
        , 'episode_anneal_threshold': 0.15}

    EpisodeWiseEpsilonAnnealing = {
        'use_episode_epsilon_anneal': False
        , 'global_epsilon': 0   # current best: 0.3
        , 'global_min_epsilon': 0   # current best: 0.1
        , 'global_decay_rate': 1.0 + 0.001  # Mean lifetime is 695
        , 'episode_init_epsilon': 1.0
        , 'episode_decay_rate': 1.0 + 0.6    # episode decay rate (mean lifetime - 0.1: 9, 0.2: 5; 0.3: 4)
    }

    @staticmethod
    def getOutputDetailLevel():
        return ExperimentConfigurator.experimentConfig['OUTPUT_DETAIL_LEVEL']

    @staticmethod
    def setExperimentConfig(parameters):
        for parameter in parameters:
            if parameter in ExperimentConfigurator.experimentConfig:
                ExperimentConfigurator.experimentConfig[parameter] = parameters[parameter]

    @staticmethod
    def setGridWorldConfig(parameters):
        for parameter in parameters:
            if parameter in ExperimentConfigurator.gridWorldConfig:
                ExperimentConfigurator.gridWorldConfig[parameter] = parameters[parameter]

    @staticmethod
    def setTamerConfig(parameters):
        for parameter in parameters:
            if parameter in ExperimentConfigurator.TamerConfig:
                ExperimentConfigurator.TamerConfig[parameter] = parameters[parameter]

    @staticmethod
    def setQLearningConfig(parameters):
        for parameter in parameters:
            if parameter in ExperimentConfigurator.qLearningConfig:
                ExperimentConfigurator.qLearningConfig[parameter] = parameters[parameter]

    def __init__(self):
        pass
