from sys import stdout as console
import subprocess
import time
from subprocess import CalledProcessError

from utils import FindUtils
from base import BaseCommand
from base import EapManagerException
from utils import ValueUtils


__author__ = "Samuele Dell'Angelo (Red HAt)"

class CheckThreadStatsCommand(BaseCommand):
    _prompt = "startinstance >"

    def execute(self, jbossHome, controller, user, password):
        self.fillParameters(jbossHome, controller, user, password)
        print chr(27) + "[2J"
        console.flush()
        print("hai chiamato check Thread statistics")

        try:
            domain = FindUtils.getDomain("domains")
            cluster = FindUtils.getCluster(domain)
            instanceTuple = FindUtils.getInstance(domain,cluster)
            pollNumb =  FindUtils.getGenericString("inserire il numero di poll >")
            pollInterval =  FindUtils.getGenericString("inserire il polling interval (sec) >")
            startCommand ='"/host='+instanceTuple[1]+'/server='+instanceTuple[0]+'/core-service=platform-mbean/type=threading:read-resource"'
            if(pollInterval != None) and (pollNumb != None):

                pollNumb = int(pollNumb)
                pollInterval = int(pollInterval)
                print("Current Threads Count | Peak Thread Count | Daemon Thread Count ")
                for i in range(pollNumb):
                    psCons = subprocess.Popen(self._complPath+" "+self._cliconn+" "+self._complContr+" "+self._complUser+" "+self._complPwd+" "+startCommand, shell=True, stdout=subprocess.PIPE)
                    output = psCons.stdout.read()
                    psCons.stdout.close()
                    psCons.wait()

                    statsDict = ValueUtils.parseCliOutput(output)

                    print(statsDict['thread-count']+" "+
                          "                  |"+statsDict['peak-thread-count']+" "+
                          "               |"+statsDict['daemon-thread-count']+" ")

                    time.sleep(pollInterval)

        except (CalledProcessError, EapManagerException, ValueError) as e:
            print(e.message)
            pass

        raw_input("premere un tasto per continuare...")
