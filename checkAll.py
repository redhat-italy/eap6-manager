#!/usr/bin/python
__author__ = "Samuele Dell'Angelo (Red Hat)"

import os
import subprocess

def findProcesses(process_name):
    ps = subprocess.Popen("ps -eaf | grep "+process_name, shell=True, stdout=subprocess.PIPE)
    output = ps.stdout.read()
    ps.stdout.close()
    ps.wait()

    return output

def printConsoleData():
    psCons = subprocess.Popen("uname -n", shell=True, stdout=subprocess.PIPE)
    output = psCons.stdout.read()
    psCons.stdout.close()
    psCons.wait()

    consoleData = "http://"+output[:len(output)-1]+":9990"
    return consoleData;

def readOutput(ps_output):
    lines = str(ps_output).split('\n')

    for line in lines:
        splitted_lines = line.split(' ')
        splitted_lines = [x for x in splitted_lines if x != '']
        if (len(splitted_lines) > 3):
            user = splitted_lines[0]
            pid = splitted_lines[1]
        type = None
        for sp_line in splitted_lines:
            if (sp_line.find("[") != -1):
                type = sp_line
                if(type.find("Process") != -1):
                    type = "[Process Controller]"
                if(type.find("Host") != -1):
                    type = "[Host Controller]"
                if(type.find("Server") != -1):
                    type = type[type.find("-D")+2:]
                break;

        if(type != None):
            print("Process JBOSS user ("+user+") type "+type+" Pid ("+pid+") is RUNNING")

    print "Indirizzo console di amministrazione: "+printConsoleData();




out = findProcesses("jboss")
readOutput(out)



