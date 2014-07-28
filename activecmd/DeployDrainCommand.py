from base import BaseCommand
from base import EapManagerException
from utils import FindUtils

__author__ = "Samuele Dell'Angelo (Red Hat)"

from utils.Propertymanager import PropertyManager
import subprocess
from subprocess import CalledProcessError
from sys import stdout as console


class DeployDrainCommand(BaseCommand):

    def execute(self, jbossHome, controller, user, password):
        self.fillParameters(jbossHome, controller, user, password)
        print chr(27) + "[2J"
        console.flush()
        print("hai chiamato deploy drain mode")

        try:
            domain = FindUtils.getDomain("domains")
            print("server group passive...")
            clusterA = FindUtils.getCluster(domain)
            print("server group active...")
            clusterB = FindUtils.getCluster(domain)
            pathTuple = FindUtils.findPath()

            deployCommand =  'deploy'
            sgCompl=self._clisg+clusterB
            nameCompl=self._cliname+pathTuple[1]

            pm = PropertyManager("Domains/"+domain+".properties")
            hostNumb = pm.getValue("host.number")
            hostPrefix = pm.getValue("host.prefix")

            appKey="application."+domain+"."+clusterB+".name"

            appName = pm.getValue(appKey)

            #disable contexts
            for i in range(hostNumb):
                instances = pm.getValue("cluster."+clusterA+"."+hostPrefix+str(i)+".instances").split(',')
                for instance in instances:
                    disableCommand = "/host="+hostPrefix+str(i)+"/server="+instance+"/subsystem=modcluster:disable()"
                    print(disableCommand)
                    subprocess.check_call([self._complPath,self._cliconn,self._complContr,self._complUser,self._complPwd,disableCommand])

            #undeploy
            if(appName != None):
                subprocess.check_call([self._complPath,self._cliconn,self._complContr,self._complUser,self._complPwd,disableAppCommand])
                undeployCommand="/server-group="+clusterB+"/deployment="+appName+":undeploy()"
                print(undeployCommand)
                subprocess.check_call([self._complPath,self._cliconn,self._complContr,self._complUser,self._complPwd,undeployCommand])
                removeCommand="/deployment="+appName+":remove()"
                print(removeCommand)
                subprocess.check_call([self._complPath,self._cliconn,self._complContr,self._complUser,self._complPwd,removeCommand])

            #deploy
            subprocess.check_call([self._complPath,self._cliconn,self._complContr,self._complUser,self._complPwd,deployCommand+" "+pathTuple[0]+" "+sgCompl+" "+nameCompl])

            #enable contexts
            for i in range(hostNumb):
                instances = pm.getValue("cluster."+clusterB+"."+hostPrefix+str(i)+".instances").split(',')
                for instance in instances:
                    enableCommand = "/host="+hostPrefix+str(i)+"/server="+instance+"/subsystem=modcluster:enable()"
                    subprocess.check_call([self._complPath,self._cliconn,self._complContr,self._complUser,self._complPwd,enableCommand])






        except (CalledProcessError, EapManagerException) as e:
            print(e.message)
            pass


        fname = "Domains/"+domain+".properties"
        PropertyManager.updateValue(fname,appKey,pathTuple[1].strip())
        raw_input("premere un tasto per continuare...")

