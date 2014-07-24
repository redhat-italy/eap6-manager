from sys import stdout as console
import subprocess
import time
from subprocess import CalledProcessError

from utils import FindUtils
from base import BaseCommand
from base import EapManagerException
from utils import ValueUtils


__author__ = "Samuele Dell'Angelo (Red HAt)"

class CheckDSStatsCommand(BaseCommand):
    _prompt = "startinstance >"

    def execute(self, jbossHome, controller, user, password):
        self.fillParameters(jbossHome, controller, user, password)
        print chr(27) + "[2J"
        console.flush()
        print("hai chiamato check Datasource statistics")

        try:
            domain = FindUtils.getDomain("domains")
            cluster = FindUtils.getCluster(domain)
            instanceTuple = FindUtils.getInstance(domain,cluster)
            datasource = FindUtils.getGenericString("inserire il nome del datasource >")
            pollNumb =  FindUtils.getGenericString("inserire il numero di poll >")
            pollInterval =  FindUtils.getGenericString("inserire il polling interval (sec) >")
            print("Check Datasource Statistics: "+datasource)
            startCommand ='"/host='+instanceTuple[1]+'/server='+instanceTuple[0]+'/subsystem=datasources/data-source='+datasource+'/statistics=pool:read-resource(include-runtime=true)"'
            if(pollInterval != None) and (pollNumb != None):

                pollNumb = int(pollNumb)
                pollInterval = int(pollInterval)
                print("Available Connections | Created Connections | In use Connections | Active Connections | Max used Connections")
                for i in range(pollNumb):
                    psCons = subprocess.Popen(self._complPath+" "+self._cliconn+" "+self._complContr+" "+self._complUser+" "+self._complPwd+" "+startCommand, shell=True, stdout=subprocess.PIPE)
                    output = psCons.stdout.read()
                    psCons.stdout.close()
                    psCons.wait()

                    statsDict = ValueUtils.parseCliOutput(output)

                    print(statsDict['AvailableCount']+" "+
                          "                   |"+statsDict['CreatedCount']+" "+
                          "                   |"+statsDict['InUseCount']+" "+
                          "                  |"+statsDict['ActiveCount']+" "+
                          "                  |"+statsDict['MaxUsedCount']+" ")
                    time.sleep(pollInterval)

        except (CalledProcessError, EapManagerException, ValueError) as e:
            print(e.message)
            pass

        raw_input("premere un tasto per continuare...")
