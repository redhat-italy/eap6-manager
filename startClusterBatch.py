#!/usr/bin/python
import sys

from utils.PropertyManager import PropertyManager
from activecmd import StartClusterCommand

pm = PropertyManager("""Domains/domains.properties""")

jbossHome = pm.getValue("jboss.home")
controller = pm.getValue("controller")
user = pm.getValue("user")
password = pm.getValue("password")
cluster = host = instance = ""
for arg in sys.argv:
    if(str(arg).find("-cluster") != -1):
        cluster = str(arg).split("=")[1]
    if(str(arg).find("-help") != -1):
        print("USAGE: startClusterBatch -cluster=<cluster>")
        exit(1)

if (cluster == ""):
    print("USAGE: startClusterBatch -cluster=<cluster>")
    exit(1)
else:
    sc = StartClusterCommand()
    sc.sendCommand(jbossHome, controller, user, password, cluster)

