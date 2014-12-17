#!/usr/bin/python
import sys

from utils.PropertyManager import PropertyManager
from activecmd import DeployCommand


__author__ = "Samuele Dell'Angelo (Red Hat)"

pm = PropertyManager("""Domains/domains.properties""")

jbossHome = pm.getValue("jboss.home")
controller = pm.getValue("controller")
user = pm.getValue("user")
password = pm.getValue("password")
cluster = path = name = ""
for arg in sys.argv:
    if(str(arg).find("-path") != -1):
        path = str(arg).split("=")[1]
    if(str(arg).find("-cluster") != -1):
        cluster = str(arg).split("=")[1]
    if(str(arg).find("-name") != -1):
        name = str(arg).split("=")[1]
    if(str(arg).find("-help") != -1):
        print("USAGE: deployBatch -path=<application-path> -cluster=<cluster> -name=<application-name>")
        exit(1)

if (path == "") or (cluster == "") or (name == ""):
    print("USAGE: deployBatch -path=<application-path> -cluster=<cluster> -name=<application-name>")
    exit(1)
else:
    sc = DeployCommand()
    sc.sendCommand(jbossHome,controller,user,password,path,cluster,name)
