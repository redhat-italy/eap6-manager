__author__ = "Samuele Dell'Angelo"
__author__ = "Andrea Battaglia (Red Hat)"

import string

class ValueUtils:

    #add to separated values, preserving unicity of the values
    @staticmethod
    def addToValues(value, old_value, separator):

        filtered_values = filter((lambda x: x != value), old_value.split(separator))
        new_values = reduce((lambda x, y: str(x)+","+str(y)), filtered_values)
        new_values = new_values+","+value
        return new_values

    @staticmethod
    def parseCliOutput(output):
        splittedOut = output.split('\n')
        splitLines = [string.split(line, '=>') for line in splittedOut if "=>" in line ]
        propertyNames = [tup[0].strip(" ").lstrip().rstrip().lstrip('{').lstrip('}').lstrip('"').rstrip('"') for tup in splitLines]
        propertyList = map(lambda x: x[1].lstrip(' "').rstrip('",'), splitLines)
        statsDict = dict([(propertyNames[i],propertyList[i]) for i in range(len(splitLines))])

        return statsDict

    @staticmethod
    def parseDeploymentList(output):
        splittedOut = output.strip().split('\n')

        return splittedOut

