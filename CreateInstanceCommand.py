__author__ = "Samuele Dell'Angelo (Red Hat)"

from BaseCommand import BaseCommand
from sys import stdout as console
from FindUtils import FindUtils
import subprocess
from subprocess import CalledProcessError
from EapManagerException import EapManagerException
from Propertymanager import PropertyManager
from ValueUtils import ValueUtils

class CreateInstanceCommand(BaseCommand):
    _prompt = "startinstance >"

    def execute(self, jbossHome, controller, user, password):
        print chr(27) + "[2J"
        console.flush()
        print("hai chiamato create Instance")

        try:
            domain = FindUtils.getDomain("domains")
            cluster = FindUtils.getCluster(domain)
            hostcontroller = FindUtils.getGenericString("host controller dovre creare l'istanza>")
            instanceName = FindUtils.getGenericString("nome istanza>")
            offset = FindUtils.getGenericString("port ofsset>")

            print("Creo Istanza: "+instanceName)
            self.sendCommand(jbossHome,controller,user,password, domain, cluster,hostcontroller,instanceName,offset)


        except (CalledProcessError,EapManagerException) as e:
            print(e.message)
            pass

        raw_input("premere un tasto per continuare...")


    def sendCommand(self, jbossHome, controller, user, password, domain, cluster, host, instance, offset):
        self.fillParameters(jbossHome, controller, user, password)
        startCommand =  "/host="+host+"/server-config="+instance+":add(group="+cluster+",socket-binding-port-offset="+offset+",auto-start=false)"

        print("eseguo: "+self._complPath+" "+self._cliconn+" "+self._complContr+" "+self._complUser+" "+self._complPwd+" "+startCommand)

        subprocess.check_call([self._complPath,self._cliconn,self._complContr,self._complUser,self._complPwd,startCommand])
        pm = PropertyManager("Domains/"+domain+".properties")
        oldInstances = pm.getValue("cluster."+cluster+".instances")
        if(oldInstances == None):
            newInstances = instance
        else:
            newInstances = ValueUtils.addToValues(instance, oldInstances, ',')
        PropertyManager.updateValue("Domains/"+domain+".properties", "cluster."+cluster+".instances", newInstances)

        oldHostInstances = pm.getValue("cluster."+cluster+"."+host+".instances")
        if(oldHostInstances == None):
            newHostInstances = instance
        else:
            newHostInstances = ValueUtils.addToValues(instance, oldHostInstances, ',')
        PropertyManager.updateValue("Domains/"+domain+".properties", "cluster."+cluster+".instances", newHostInstances)
