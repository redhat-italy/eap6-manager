import string
import os

__author__ = "Samuele Dell'Angelo (Red Hat)"

class PropertyManager:
    
    _propertyDict = dict()
    
    def __init__(self, filename):
        dir=os.path.dirname(__file__)
        fpath=dir+"""/"""+filename
        fp = open(fpath,'r')
        splitLines = [string.split(line, '=') for line in fp.readlines() if "=" in line]
        propertyNames = [tup[0] for tup in splitLines]
        propertyList = map(lambda x: x[1].strip(), splitLines)
        self._propertyDict = dict([(propertyNames[i],propertyList[i]) for i in range(len(splitLines))])
        fp.close()
        
    
    def test(self):
        print(self._propertyDict)
    
    
       
    def getValue(self, key):
        try:
            return self._propertyDict[key]
        except:
            return None

    @staticmethod
    def create(filepath):
        dir=os.path.dirname(__file__)
        fpath=dir+"""/"""+filepath
        fp = open(fpath,'w')
        fp.close()

    @staticmethod
    def writeValue(filename, key, value):
        dir=os.path.dirname(__file__)
        fpath=dir+"""/"""+filename
        fp = open(fpath,'a')
        line = key+"="+value+"\n"
        fp.write(line)
        fp.close()

    @staticmethod
    def updateValue(filename, key, newValue):
        dir=os.path.dirname(__file__)
        fpath=dir+"""/"""+filename
        fp = open(fpath,'r')
        lines = fp.readlines()
        fp.close()
        fpw = open(fpath, 'w')
        newline = key+"="+newValue+"\n"
        for line in lines:
            if(line.split('=')[0] != key):
                fpw.write(line)

        fpw.write(newline)
        fpw.close()
