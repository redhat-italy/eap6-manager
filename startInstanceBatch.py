#!/usr/bin/python
import sys
from Propertymanager import PropertyManager
from StartInstanceCommand import StartInstanceCommand

__author__ = "Samuele Dell'Angelo (Red Hat)"

pm = PropertyManager("""Domains/domains.properties""")

jbossHome = pm.getValue("jboss.home")
controller = pm.getValue("controller")
user = pm.getValue("user")
password = pm.getValue("password")
cluster = host = instance = ""
for arg in sys.argv:
    if(str(arg).find("-host") != -1):
        host = str(arg).split("=")[1]
    if(str(arg).find("-instance") != -1):
        instance = str(arg).split("=")[1]
    if(str(arg).find("-help") != -1):
        print("USAGE: startInstanceBatch -host=<jboss domain host> -instance=<instance>")
        exit(1)

if(instance == "") or (host == ""):
    print("USAGE: startInstanceBatch -host=<jboss domain host> -instance=<instance>")
    exit(1)
else:
    sc = StartInstanceCommand()
    sc.sendCommand(jbossHome,controller,user,password,host,instance)
