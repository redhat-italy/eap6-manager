#!/usr/bin/python
from activecmd import StartInstanceCommand, StopInstanceCommand, StartClusterCommand, DeployCommand, \
    RestartClusterCommand, InsertJvmOptClusterCommand, CreateInstanceCommand, InsertJvmOptCommand, \
    RestartInstanceCommand, StopClusterCommand
from base import EapManagerException
from passivecmd import CheckThreadStatsCommand, CheckJgoupsMulticastRecCommand, CheckJgoupsMulticastSendCommand, \
    CheckHttpStatsCommand


__author__ = "Samuele Dell'Angelo (Red Hat)"

from utils.Propertymanager import PropertyManager
from passivecmd.CheckDsCommand import CheckDSCommand
from activecmd.CreateSGCommand import CreateSGCommand
from passivecmd.CheckDsStatsCommand import CheckDSStatsCommand
from sys import stdout as console

# available commands
COMMANDS = { 'exit' : 'exit' , 'startCluster' : StartClusterCommand() , 'stopCluster' : StopClusterCommand() , 'restartCluster' : RestartClusterCommand()
    ,'startInstance' : StartInstanceCommand() , 'stopInstance' : StopInstanceCommand() , 'restartInstance' : RestartInstanceCommand()
    , "deploy" : DeployCommand() , "check datasource" : CheckDSCommand(), "create cluster" : CreateSGCommand(), "create instance" : CreateInstanceCommand(),
             "insert JVM Options" : InsertJvmOptCommand(), "insert JVM Options per Cluster" : InsertJvmOptClusterCommand(),
             "check datasource statistics" : CheckDSStatsCommand(), "check thread stats" : CheckThreadStatsCommand(),
             "check http statistics" : CheckHttpStatsCommand(), "check Jgroups Receive" : CheckJgoupsMulticastRecCommand(),
             "check jgroups Send" : CheckJgoupsMulticastSendCommand()}

HISTORY = list()
TRASH = list()

print("initializing properties...")
pm = PropertyManager("Domains/domains.properties")

jbossHome = pm.getValue("jboss.home")
controller = pm.getValue("controller")
user = pm.getValue("user")
password = pm.getValue("password")

_prompt = ">"

while True:
    print chr(27) + "[2J"
    console.flush()
    print("Comandi disponibili: \n")
    for i in range(len(COMMANDS.keys())):
        print(str(i)+") "+COMMANDS.keys()[i]+"\n")

    print("digitare il numero del comando desiderato o exit per uscire")

    console.flush()

    try:
        cmd = int(raw_input(_prompt))
    except ValueError:
        print("ERRORE: Inserire un numero")
        continue

    if(cmd>len(COMMANDS)):
        print("ERRORE: Inserire un numero che sia compreso in quelli indicati")
        continue

    if(COMMANDS[COMMANDS.keys()[int(cmd)]] == "exit"):
        break

    try:
        command = COMMANDS[COMMANDS.keys()[int(cmd)]]
        command.execute(jbossHome, controller, user, password)

    except (KeyError, EapManagerException) as e:
        print("ERRORE nell'esecuzione del comando")
        print(e.message)
        pass