__author__ = "Samuele Dell'Angelo (Red Hat)"

from Propertymanager import PropertyManager
from EapManagerException import EapManagerException
from BaseCommand import BaseCommand
from FindUtils import FindUtils
import subprocess
from subprocess import CalledProcessError
from sys import stdout as console


class DeployCommand(BaseCommand):

    def execute(self, jbossHome, controller, user, password):
        self.fillParameters(jbossHome, controller, user, password)
        print chr(27) + "[2J"
        console.flush()
        print("hai chiamato deploy")

        try:
            domain = FindUtils.getDomain("domains")
            cluster = FindUtils.getCluster(domain)
            pathTuple = FindUtils.findPath()

            print("Avvio cluster: "+cluster)

            deployCommand =  'deploy'
            sgCompl=self._clisg+cluster
            nameCompl=self._cliname+pathTuple[1]

            print("eseguo: "+self._complPath+" "+self._cliconn+" "+self._complContr+" "+self._complUser+" "+self._complPwd+" "+deployCommand+" "+pathTuple[0]+" "+sgCompl+" "+nameCompl)

            subprocess.check_call([self._complPath,self._cliconn,self._complContr,self._complUser,self._complPwd,deployCommand+" "+pathTuple[0]+" "+sgCompl+" "+nameCompl])

        except (CalledProcessError,EapManagerException) as e:
            print(e.message)
            pass

        key="application."+domain+"."+cluster+".name"
        fname = "Domains/"+domain+".properties"
        PropertyManager.writeValue(fname,key,pathTuple[1].strip())
        raw_input("premere un tasto per continuare...")

