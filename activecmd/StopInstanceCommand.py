from sys import stdout as console
import subprocess
from subprocess import CalledProcessError

from base import BaseCommand
from base import EapManagerException
from utils import FindUtils


__author__ = "Samuele Dell'Angelo (Red HAt)"

class StopInstanceCommand(BaseCommand):
    _prompt = "startinstance >"

    def execute(self, jbossHome, controller, user, password):
        print chr(27) + "[2J"
        console.flush()
        print("hai chiamato startInstance")

        try:
            domain = FindUtils.getDomain("domains")
            cluster = FindUtils.getCluster(domain)
            instanceTuple = FindUtils.getInstance(domain,cluster)

            print("Stop istanza: "+cluster)
            self.sendCommand(jbossHome,controller,user,password,instanceTuple[1],instanceTuple[0])

        except (CalledProcessError, EapManagerException) as e:
            print(e.message)
            pass

        raw_input("premere un tasto per continuare...")

    def sendCommand(self, jbossHome, controller, user, password, host, instance):
        self.fillParameters(jbossHome, controller, user, password)
        startCommand =  "/host="+host+"/server-config="+instance+":stop"

        print("eseguo: "+self._complPath+" "+self._cliconn+" "+self._complContr+" "+self._complUser+" "+self._complPwd+" "+startCommand)

        subprocess.check_call([self._complPath,self._cliconn,self._complContr,self._complUser,self._complPwd,startCommand])