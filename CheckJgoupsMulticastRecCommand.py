from BaseCommand import BaseCommand
from sys import stdout as console
from FindUtils import FindUtils
import subprocess
from Propertymanager import PropertyManager
from subprocess import CalledProcessError
from EapManagerException import EapManagerException

__author__ = "Samuele Dell'Angelo (Red HAt)"

class CheckJgoupsMulticastRecCommand(BaseCommand):
    _prompt = "startinstance >"

    def execute(self, jbossHome, controller, user, password):
        self.fillParameters(jbossHome, controller, user, password)
        print chr(27) + "[2J"
        console.flush()
        print("hai chiamato check Jgroups Receiver")

        try:
            pm = PropertyManager("Domains/domains.properties")
            javaHome = pm.getValue("java.home")
            bindAddress =  FindUtils.getGenericString("inserire il bind address >")
            mcastAddress =  FindUtils.getGenericString("inserire il multicast address >")
            mcastPort = FindUtils.getGenericString("inserire la multicast port >")

            subprocess.check_call([javaHome+"/bin/java","-Djava.net.preferIPv4Stack=true","-cp", jbossHome+"modules/system/layers/base/org/jgroups/main/jgroups-3.2.7.Final-redhat-1.jar", "org.jgroups.tests.McastReceiverTest",
                                   "-mcast_addr",mcastAddress, "-bind_addr",bindAddress,"-port",mcastPort ])


        except (CalledProcessError,EapManagerException, ValueError) as e:
            print(e.message)
            pass

        raw_input("premere un tasto per continuare...")
