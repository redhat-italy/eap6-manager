from base import BaseCommand
from base import EapManagerException
from utils import FindUtils

__author__ = "Samuele Dell'Angelo (Red Hat)"

from utils.PropertyManager import PropertyManager
import subprocess
from subprocess import CalledProcessError
from sys import stdout as console


class DeployCommand(BaseCommand):

    def execute(self, jbossHome, controller, user, password):
        print chr(27) + "[2J"
        console.flush()
        print("hai chiamato deploy")

        try:
            domain = FindUtils.getDomain("domains")
            cluster = FindUtils.getCluster(domain)
            pathTuple = FindUtils.findPath()

            print("Avvio cluster: "+cluster)
            self.sendCommand(jbossHome, controller, user, password, pathTuple[0], cluster, pathTuple[1])

            key="application."+domain+"."+cluster+".name"
            fname = "Domains/"+domain+".properties"
            pm = PropertyManager()
            pm.writeValue(fname,key,pathTuple[1].strip())
            raw_input("premere un tasto per continuare...")

        except (CalledProcessError, EapManagerException) as e:
            print(e.message)
            pass


    def sendCommand(self, jbossHome, controller, user, password, path, cluster, name):
        self.fillParameters(jbossHome, controller, user, password)
        deployCommand = 'deploy'+" "+ path +" " + self._clisg + cluster +" "+ self._cliname + name
        print("eseguo: "+self._complPath+" "+self._cliconn+" "+self._complContr+" "+self._complUser+" "+self._complPwd+" "+deployCommand)

        subprocess.check_call([self._complPath,self._cliconn,self._complContr,self._complUser,self._complPwd,deployCommand])


