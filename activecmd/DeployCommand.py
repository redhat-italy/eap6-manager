from subprocess import CalledProcessError
import subprocess
from sys import stdout as console

from base import BaseCommand
from base import EapManagerException
from utils import FindUtils
from utils.PropertyManager import PropertyManager
from utils.ValueUtils import ValueUtils


__author__ = "Samuele Dell'Angelo (Red Hat)"
__author__ = "Andrea Battaglia (Red Hat)"



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
        
        #list deployments
        listDeploymentsCommand='ls'+" "+ self._clisg + cluster+'/deployment'
        print("eseguo: "+self._complPath+" "+self._cliconn+" "+self._complContr+" "+self._complUser+" "+self._complPwd+" "+listDeploymentsCommand)
        output = subprocess.Popen([self._complPath,self._cliconn,self._complContr,self._complUser,self._complPwd,listDeploymentsCommand], stdout=subprocess.PIPE ).communicate()[0]

        deploymentList = ValueUtils.parseDeploymentList(output)

        if(name in deploymentList):
            #undeploy
            undeployCommand=self._clisg+cluster+self._clidpmt+name+":undeploy()"
            print(undeployCommand)
            subprocess.check_call([self._complPath,self._cliconn,self._complContr,self._complUser,self._complPwd,undeployCommand])
            removeSgCommand=self._clisg+cluster+self._clidpmt+name+":remove()"
            print(undeployCommand)
            subprocess.check_call([self._complPath,self._cliconn,self._complContr,self._complUser,self._complPwd,removeSgCommand])
            removeCommand=self._clidpmt+name+":remove()"
            print(removeCommand)
            subprocess.check_call([self._complPath,self._cliconn,self._complContr,self._complUser,self._complPwd,removeCommand])
        
        
        #deploy
        deployCommand = 'deploy'+" "+ path +" " + self._clisgs + cluster +" "+ self._cliname + name
        print("eseguo: "+self._complPath+" "+self._cliconn+" "+self._complContr+" "+self._complUser+" "+self._complPwd+" "+deployCommand)

        subprocess.check_call([self._complPath,self._cliconn,self._complContr,self._complUser,self._complPwd,deployCommand])

        #restart
        startCommand = self._clisg+cluster+":restart-servers"
        print("eseguo: "+self._complPath + " " + self._cliconn + " " + self._complContr + " " + self._complUser + " " + self._complPwd + " " + startCommand)

        subprocess.check_call([self._complPath,self._cliconn,self._complContr,self._complUser,self._complPwd,startCommand])
