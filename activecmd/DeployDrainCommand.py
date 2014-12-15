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
            runtimeNameList = pathTuple[0].split('/')
            runtimeNameSingle = runtimeNameList[len(runtimeNameList)-1]
            runtimeName = self._clirname+runtimeNameSingle

            deployCommand =  'deploy'
            sgCompl=self._clisg+clusterB
            nameCompl=self._cliname+pathTuple[1]

            pm = PropertyManager("Domains/"+domain+".properties")
            hostNumb = pm.getValue("host.number")
            hostPrefix = pm.getValue("host.prefix")
            hostSuffix = pm.getValue("host.suffix")

            appKey="application."+domain+"."+clusterB+".name"

            appName = pm.getValue(appKey)

            #undeploy
            if(appName != None):
                undeployCommand="/server-group="+clusterB+"/deployment="+appName+":undeploy()"
                print(undeployCommand)
                subprocess.check_call([self._complPath,self._cliconn,self._complContr,self._complUser,self._complPwd,undeployCommand])
                removeSgCommand="/server-group="+clusterB+"/deployment="+appName+":remove()"
                print(undeployCommand)
                subprocess.check_call([self._complPath,self._cliconn,self._complContr,self._complUser,self._complPwd,removeSgCommand])
                removeCommand="/deployment="+appName+":remove()"
                print(removeCommand)
                subprocess.check_call([self._complPath,self._cliconn,self._complContr,self._complUser,self._complPwd,removeCommand])

            #deploy
            print(self._complPath+" "+self._cliconn+" "+self._complContr+" "+self._complUser+" "+self._complPwd+" "+deployCommand+" "+pathTuple[0]+" "+sgCompl+" "+nameCompl+" "+runtimeName)
            subprocess.check_call([self._complPath,self._cliconn,self._complContr,self._complUser,self._complPwd,deployCommand+" "+pathTuple[0]+" "+sgCompl+" "+nameCompl+" "+runtimeName])

            #enable contexts
            for i in range(int(hostNumb)):
                instances = pm.getValue("cluster."+clusterB+"."+hostPrefix+str(i+1)+hostSuffix+".instances").split(',')
                for instance in instances:
                    enableCommand = "/host="+hostPrefix+str(i+1)+hostSuffix+"/server="+instance+"/subsystem=modcluster:enable()"
                    print(enableCommand)
                    subprocess.check_call([self._complPath,self._cliconn,self._complContr,self._complUser,self._complPwd,enableCommand])


            #disable contexts
            for i in range(int(hostNumb)):
                print("cluster."+clusterA+"."+hostPrefix+str(i+1)+".instances")
                instances = pm.getValue("cluster."+clusterA+"."+hostPrefix+str(i+1)+hostSuffix+".instances").split(',')
                for instance in instances:
                    disableCommand = "/host="+hostPrefix+str(i+1)+hostSuffix+"/server="+instance+"/subsystem=modcluster:disable()"
                    print(disableCommand)
                    subprocess.check_call([self._complPath,self._cliconn,self._complContr,self._complUser,self._complPwd,disableCommand])

            fname = "Domains/"+domain+".properties"
            pm = PropertyManager()
            pm.updateValue(fname,appKey,pathTuple[1].strip())




        except (CalledProcessError, EapManagerException) as e:
            print(e.message)
            pass


        raw_input("premere un tasto per continuare...")

