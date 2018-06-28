# qValueSaver.py
#
# Convert qValues (Counter) to json string and save the string to the specified file
# Read qValues (json string) from specified file and convert it to Counter class
# -----------------------

import util
import json


def qValues2Json(qValues):
    """ convert the qValues (Counter) to json (dict) """
    # json is in the format of {string: value}
    json_qValues = dict()
    # keys are in the format of (state, action), where state is tuple, action is str
    for key in qValues:
        action = key[1]
        state_x = key[0][0]
        state_y = key[0][1]
        qValue = qValues[key]
        # define the key in json file
        str_json_key = str(state_x) + ',' + str(state_y) + ',' + action
        json_qValues[str_json_key] = qValue
    return json_qValues


def json2qValues(json_dict):
    """ convert the json (dict) to qValues (Counter) """
    qValues = util.Counter()
    for key in json_dict:
        elements = key.split(',')
        state = (int(elements[0]), int(elements[1]))
        action = elements[2]
        # save it to the qValues (Counter)
        qValues[(state, action)] = json_dict[key]
    return qValues


def saveQValuesCounterToJsonFile(qValue_file, qValues):
    """ save the qValues Counter to the specified file"""
    f_qValues = open(qValue_file, 'w')
    json_qValues = json.dumps(qValues2Json(qValues))
    f_qValues.write(json_qValues)
    f_qValues.close()


def readQValuesFromJsonFile(qValue_file):
    """ read the qValues from specified json file and covert it to Counter """
    with open(qValue_file) as f_qValues:
        qValues_dict = json.load(f_qValues)
    return json2qValues(qValues_dict)


def main():
    print('------- Test save to json file -----------')
    f = '/Users/lguan/Desktop/Others/qValues.json'
    qValues = util.Counter()
    qValues[((1, 1), 'north')] = 1
    qValues[((3, 2), 'west')] = 3.0234
    saveQValuesCounterToJsonFile(f, qValues)
    print('- save to json file successfully\n')

    print('------- Test read from json file -----------')
    print(readQValuesFromJsonFile(f))


if __name__ == '__main__':
    main()

