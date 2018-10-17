# experimentConfigurator.py
# ------------
# The central configurator for experiment.
# You can set the values for all related parameters here

from experiment_saver import counter_saver

#######################################################
######## Output detail level control  #################
#######################################################
VERY_SHORT_OUTPUT = 0
SHORT_OUTPUT = 1
SOME_DETAILS = 2
#######################################################
############ Different feedback type ##################
#######################################################
HUMAN_FEEDBACK = 0
TRAINED_AGENT_FEEDBACK = 1
#######################################################


class ExperimentConfigurator:
    configurations = {
        'experimentConfig': {
            'output_detail_level': VERY_SHORT_OUTPUT,
            'text_only': True,
            'fast_experiment': True,  # no wait at the end of each epoch and no graphic output
            'frame_rate': 1,
            'subject_name': '',
            'game': '',
            'date': '',
            'experiment_identifier': '',
            'expr_log_dir': '',
            'root_log_dir': ''
        }
    }

    #######################################################
    #######################################################

    @staticmethod
    def getOutputDetailLevel():
        return ExperimentConfigurator.configurations['experimentConfig']['OUTPUT_DETAIL_LEVEL']

    @staticmethod
    def setExperimentConfig(parameters):
        for parameter in parameters:
            if parameter in ExperimentConfigurator.configurations['experimentConfig']:
                ExperimentConfigurator.configurations['experimentConfig'][parameter] = parameters[parameter]

    @staticmethod
    def getExperimentConfig(param_name):
        if param_name in ExperimentConfigurator.configurations['experimentConfig']:
            return ExperimentConfigurator.configurations['experimentConfig'][param_name]
        else:
            return None

    @staticmethod
    def saveConfigToFile(fname):
        counter_saver.saveDictToFile(fname, ExperimentConfigurator.configurations)

    def __init__(self):
        pass
