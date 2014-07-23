from BaseCommand import BaseCommand
from sys import stdout as console
from FindUtils import FindUtils
import subprocess
import time
from ValueUtils import ValueUtils
from subprocess import CalledProcessError
from EapManagerException import EapManagerException

__author__ = "Samuele Dell'Angelo (Red HAt)"

class CheckHttpStatsCommand(BaseCommand):
    _prompt = "startinstance >"

    def execute(self, jbossHome, controller, user, password):
        self.fillParameters(jbossHome, controller, user, password)
        print chr(27) + "[2J"
        console.flush()
        print("hai chiamato check Http statistics")

        try:
            domain = FindUtils.getDomain("domains")
            cluster = FindUtils.getCluster(domain)
            instanceTuple = FindUtils.getInstance(domain,cluster)
            pollNumb =  FindUtils.getGenericString("inserire il numero di poll >")
            pollInterval =  FindUtils.getGenericString("inserire il polling interval (sec) >")
            startCommand ='"/host='+instanceTuple[1]+'/server='+instanceTuple[0]+'/subsystem=web/connector=http:read-resource(include-runtime=true)"'
            if(pollInterval != None) and (pollNumb != None):

                pollNumb = int(pollNumb)
                pollInterval = int(pollInterval)
                print("Bytes Received | Bytes Sent | Error Count | Request Count |")
                for i in range(pollNumb):
                    psCons = subprocess.Popen(self._complPath+" "+self._cliconn+" "+self._complContr+" "+self._complUser+" "+self._complPwd+" "+startCommand, shell=True, stdout=subprocess.PIPE)
                    output = psCons.stdout.read()
                    psCons.stdout.close()
                    psCons.wait()

                    statsDict = ValueUtils.parseCliOutput(output)

                    print(statsDict['bytesReceived']+" "+
                          "         |"+statsDict['bytesSent']+" "+
                          "    |"+statsDict['errorCount']+" "+
                          "           |"+statsDict['requestCount']+" ")

                    time.sleep(pollInterval)

        except (CalledProcessError,EapManagerException, ValueError) as e:
            print(e.message)
            pass

        raw_input("premere un tasto per continuare...")
