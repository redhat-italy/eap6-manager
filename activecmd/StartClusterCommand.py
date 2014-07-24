from base import BaseCommand
from base import EapManagerException
from utils import FindUtils

__author__ = "Samuele Dell'Angelo (Red Hat)"

import subprocess
from subprocess import CalledProcessError
from sys import stdout as console


class StartClusterCommand(BaseCommand):

    def execute(self, jbossHome, controller, user, password):
        print chr(27) + "[2J"
        console.flush()
        print("hai chiamato startCluster")

        try:
            domain = FindUtils.getDomain("domains")
            cluster = FindUtils.getCluster(domain)

            print("Avvio cluster: "+cluster)
            self.sendCommand(jbossHome,controller,user,password,cluster)

        except (CalledProcessError, EapManagerException) as e:
            print(e.message)
            pass

        raw_input("premere un tasto per continuare...")

    def sendCommand(self, jbossHome, controller, user, password, cluster):
        self.fillParameters(jbossHome, controller, user, password)
        startCommand =  "/server-group="+cluster+":start-servers"

        print("eseguo: "+self._complPath+" "+self._cliconn+" "+self._complContr+" "+self._complUser+" "+self._complPwd+" "+startCommand)

        subprocess.check_call([self._complPath,self._cliconn,self._complContr,self._complUser,self._complPwd,startCommand])

