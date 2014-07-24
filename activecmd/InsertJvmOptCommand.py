from sys import stdout as console
import subprocess
from subprocess import CalledProcessError

from base import BaseCommand
from base import EapManagerException
from utils import FindUtils


__author__ = "Samuele Dell'Angelo (Red HAt)"

class InsertJvmOptCommand(BaseCommand):
    _prompt = "insertOption >"

    def execute(self, jbossHome, controller, user, password):
        print chr(27) + "[2J"
        console.flush()
        print("hai chiamato insert JVM option")

        try:
            domain = FindUtils.getDomain("domains")
            cluster = FindUtils.getCluster(domain)
            instanceTuple = FindUtils.getInstance(domain,cluster)
            option = FindUtils.getGenericString("jvm option >")

            self.sendCommand(jbossHome,controller,user,password,instanceTuple[1],instanceTuple[0],option)


        except (CalledProcessError, EapManagerException) as e:
            print(e.message)
            pass

        raw_input("premere un tasto per continuare...")


    def sendCommand(self, jbossHome, controller, user, password, host, instance, option):
        self.fillParameters(jbossHome, controller, user, password)
        checkJvmCommand =  "/host="+host+"/server-config="+instance+"/jvm="+instance+"jvm:read-resource"
        createJvmCommand = "/host="+host+"/server-config="+instance+"/jvm="+instance+"jvm:add"
        insertOptionCommand = '/host='+host+'/server-config='+instance+'/jvm='+instance+'jvm:add-jvm-option(jvm-option="'+option+'")'

        print("eseguo: "+self._complPath+" "+self._cliconn+" "+self._complContr+" "+self._complUser+" "+self._complPwd+" "+checkJvmCommand)
        psCons = subprocess.Popen(self._complPath+" "+self._cliconn+" "+self._complContr+" "+self._complUser+" "+self._complPwd+" "+checkJvmCommand, shell=True, stdout=subprocess.PIPE)
        output = psCons.stdout.read()
        psCons.stdout.close()
        psCons.wait()
        print(output)

        if (str(output).find("success") == -1):
            print("eseguo: "+self._complPath+" "+self._cliconn+" "+self._complContr+" "+self._complUser+" "+self._complPwd+" "+createJvmCommand)
            subprocess.check_call([self._complPath,self._cliconn,self._complContr,self._complUser,self._complPwd,createJvmCommand])

        print("eseguo: "+self._complPath+" "+self._cliconn+" "+self._complContr+" "+self._complUser+" "+self._complPwd+" "+insertOptionCommand)

        subprocess.check_call([self._complPath,self._cliconn,self._complContr,self._complUser,self._complPwd,insertOptionCommand])