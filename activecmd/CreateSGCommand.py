from base import BaseCommand
from base import EapManagerException
from utils import ValueUtils, FindUtils

__author__ = "Samuele Dell'Angelo (Red Hat)"
__author__ = "Andrea Battaglia (Red Hat)"

import subprocess
from subprocess import CalledProcessError
from sys import stdout as console
from utils.PropertyManager import PropertyManager


class CreateSGCommand(BaseCommand):

    def execute(self, jbossHome, controller, user, password):
        print chr(27) + "[2J"
        console.flush()
        print("hai chiamato create Cluster")

        try:
            domain = FindUtils.getDomain("domains")
            profile = FindUtils.getGenericString("inserire il nome del profilo>")
            cluster = FindUtils.getGenericString("inserire il nome del cluster>")
            sbgroup = FindUtils.getGenericString("inserire il nome del socket binding group>")

            print("Creo cluster: "+cluster)
            self.sendCommand(jbossHome,controller,user,password,cluster, sbgroup, domain, profile)

        except (CalledProcessError, EapManagerException) as e:
            print(e.message)
            pass

        raw_input("premere un tasto per continuare...")

    def sendCommand(self, jbossHome, controller, user, password, cluster, sbgroup, domain, profile):
        self.fillParameters(jbossHome, controller, user, password)
        startCommand =  self._clisg+cluster+":add(profile="+profile+",socket-binding-group="+sbgroup+")"

        print("eseguo: "+self._complPath+" "+self._cliconn+" "+self._complContr+" "+self._complUser+" "+self._complPwd+" "+startCommand)

        subprocess.check_call([self._complPath,self._cliconn,self._complContr,self._complUser,self._complPwd, startCommand])
        pm = PropertyManager("Domains/"+domain+".properties")
        old_clusters = pm.getValue("clusters")
        if(old_clusters == None):
            new_clusters = cluster
        else:
            new_clusters = ValueUtils.addToValues(cluster, old_clusters, ',')
        pm.updateValue("Domains/"+domain+".properties", "clusters", new_clusters)

