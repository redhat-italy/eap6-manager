from EapManagerException import EapManagerException

__author__ = "Samuele Dell'Angelo (Red Hat)"

from BaseCommand import BaseCommand
from FindUtils import FindUtils
import subprocess
from subprocess import CalledProcessError
from sys import stdout as console


class RestartClusterCommand(BaseCommand):

    def execute(self, jbossHome, controller, user, password):
        self.fillParameters(jbossHome, controller, user, password)
        print chr(27) + "[2J"
        console.flush()
        print("hai chiamato restartCluster")

        try:
            domain = FindUtils.getDomain("domains")
            cluster = FindUtils.getCluster(domain)

            print("Avvio cluster: "+cluster)

            startCommand = "/server-group="+cluster+":restart-servers"

            print("eseguo: "+self._complPath + " " + self._cliconn + " " + self._complContr + " " + self._complUser + " " + self._complPwd + " " + startCommand)

            subprocess.check_call([self._complPath,self._cliconn,self._complContr,self._complUser,self._complPwd,startCommand])

        except (CalledProcessError,EapManagerException) as e:
            print(e.message)
            pass

        raw_input("premere un tasto per continuare...")
