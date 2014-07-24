#!/usr/bin/python
import datetime
import os
import sys

from utils.Propertymanager import PropertyManager


__author__ = "Samuele Dell'Angelo (Red Hat)"


import shutil
import glob

pm = PropertyManager("""Domains/domains.properties""")

base_dir = pm.getValue("host.controller.jboss.home")

def findAllFiles(instance,fileType):
    path = base_dir+"/domain/servers/"+instance+"/log/"
    return glob.glob(path+"*."+fileType+"*")


def generateDestDir(instance):
    path = base_dir+"/domain/servers/"+instance+"/log/"
    now = datetime.datetime.now()
    month = str(now.month) if len(str(now.month)) == 2 else "0"+str(now.month)
    day = str(now.day) if len(str(now.day)) == 2 else "0"+str(now.day)
    hour = str(now.hour) if len(str(now.hour)) == 2 else "0"+str(now.hour)
    minute = str(now.minute) if len(str(now.minute)) == 2 else "0"+str(now.minute)
    destDir = path+"StoreLog_dd"+str(now.year)+month+day+"."+hour+minute+"/"
    if not os.path.exists(destDir):
        os.makedirs(destDir)
    return destDir

instance = ""
for arg in sys.argv:
    if(str(arg).find("-instance") != -1):
        instance = str(arg).split("=")[1]
    if(str(arg).find("-help") != -1):
        print("USAGE storeLog -instance=<instance name>")
        exit(1)

if(instance == ""):
    print("USAGE storeLog -instance=<instance name>")

destination = generateDestDir(instance)


#find and move *.log
for file in findAllFiles(instance,"log"):
    shutil.move(file, destination+os.path.basename(file))

#find and move *.out
for file in findAllFiles(instance,"out"):
    shutil.move(file, destination+os.path.basename(file))