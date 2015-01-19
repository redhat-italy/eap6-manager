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



#/home/abattaglia/temp/simple-blank-ear-ear.ear
#simpleapp

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
            sgCompl=self._clisgs+clusterB
            nameCompl=self._cliname+pathTuple[1]

            pm = PropertyManager("Domains/"+domain+".properties")
            hostNumb = pm.getValue("host.number")
            hostPrefix = pm.getValue("host.prefix")
            hostSuffix = pm.getValue("host.suffix")

            appKey="application."+domain+"."+clusterB+".name"

            #appName = pm.getValue(appKey)
            appName=pathTuple[1]
            
            #UNDEPLOY FROM PASSIVE CLUSTER
            #list deployments in group
            listDeploymentsPassiveCommand='ls'+" "+ self._clisg + clusterA+'/deployment'
            print("eseguo: "+self._complPath+" "+self._cliconn+" "+self._complContr+" "+self._complUser+" "+self._complPwd+" "+listDeploymentsPassiveCommand)
            output = subprocess.Popen([self._complPath,self._cliconn,self._complContr,self._complUser,self._complPwd,listDeploymentsPassiveCommand], stdout=subprocess.PIPE ).communicate()[0]
            deploymentList = ValueUtils.parseDeploymentList(output)

            if(appName in deploymentList):
                undeployCommand=self._clisg+clusterA+self._clidpmt+appName+":undeploy()"
                print(undeployCommand)
                subprocess.check_call([self._complPath,self._cliconn,self._complContr,self._complUser,self._complPwd,undeployCommand])
                removeSgCommand=self._clisg+clusterA+self._clidpmt+appName+":remove()"
                print(undeployCommand)
                subprocess.check_call([self._complPath,self._cliconn,self._complContr,self._complUser,self._complPwd,removeSgCommand])
        
        
            #list deployments in domain
            listDeploymentsCommandDomain='ls'+" "+ '/deployment'
            print("eseguo: "+self._complPath+" "+self._cliconn+" "+self._complContr+" "+self._complUser+" "+self._complPwd+" "+listDeploymentsCommandDomain)
            output = subprocess.Popen([self._complPath,self._cliconn,self._complContr,self._complUser,self._complPwd,listDeploymentsCommandDomain], stdout=subprocess.PIPE ).communicate()[0]
            deploymentList = ValueUtils.parseDeploymentList(output)
            #undeploy
            if(appName in deploymentList):
                #list deployments in group
                listDeploymentsCommand='ls'+" "+ self._clisg + clusterB+'/deployment'
                print("eseguo: "+self._complPath+" "+self._cliconn+" "+self._complContr+" "+self._complUser+" "+self._complPwd+" "+listDeploymentsCommand)
                output = subprocess.Popen([self._complPath,self._cliconn,self._complContr,self._complUser,self._complPwd,listDeploymentsCommand], stdout=subprocess.PIPE ).communicate()[0]
                deploymentList = ValueUtils.parseDeploymentList(output)

                if(appName in deploymentList):
                    undeployCommand=self._clisg+clusterB+self._clidpmt+appName+":undeploy()"
                    print(undeployCommand)
                    subprocess.check_call([self._complPath,self._cliconn,self._complContr,self._complUser,self._complPwd,undeployCommand])
                    removeSgCommand=self._clisg+clusterB+self._clidpmt+appName+":remove()"
                    print(undeployCommand)
                    subprocess.check_call([self._complPath,self._cliconn,self._complContr,self._complUser,self._complPwd,removeSgCommand])
                
                removeCommand=self._clidpmt+appName+":remove()"
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

