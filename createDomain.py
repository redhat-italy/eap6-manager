#!/usr/bin/python

from ValueUtils import ValueUtils
import os
import sys
from copy import deepcopy
from Propertymanager import PropertyManager

__author__ = "Samuele Dell'Angelo (Red Hat)"


import shutil
import lxml.etree as ET

pm = PropertyManager("""Domains/domains.properties""")

base_dir = pm.getValue("domain.controller.jboss.home")

def getDomainFile(domain):
    if(os.path.isfile("domain.xml."+domain+".template")):
        tree = ET.parse("domain.xml."+domain+".template")
    else:
        tree = ET.parse('domain.xml.template')

    root = tree.getroot()
    if(root == None):
        print("domain template not present")
        exit(1)

    return tree




domain = ""
for arg in sys.argv:
    if(str(arg).find("-domain") != -1):
        domain = str(arg).split("=")[1]
    if(str(arg).find("-profile") != -1):
        profileName = str(arg).split("=")[1]
    if(str(arg).find("-help") != -1):
        print("USAGE createDomain -domain=<domain name> -profile=<profile name>")
        exit(1)

if(domain == ""):
    print("USAGE createDomain -domain=<domain name>")

destination = base_dir+"/domain/configuration/"

domainFile = getDomainFile(domain)
profiles = domainFile.find('{urn:jboss:domain:1.4}profiles')
for profile in profiles.iter('{urn:jboss:domain:1.4}profile'):
    name = profile.get('name')
    if(name == 'full-ha'):
        copyProfile = deepcopy(profile)
        copyProfile.set('name',profileName)
        profiles.append(copyProfile)

domainFile.write("domain.xml")

if(os.path.isfile(destination+"domain.xml")):
    shutil.move(destination+"domain.xml", destination+"domain.xml.ORIG")

if(os.path.isfile("domain.xml")):
    shutil.copy("domain.xml", destination+"domain.xml")
    shutil.move("domain.xml","domain.xml."+domain+".template")
if(not(os.path.isfile("Domains/"+domain+".properties"))):
    pm.create("Domains/"+domain+".properties")

old_domains = pm.getValue("domains")
if(old_domains.find(domain) == -1):
    new_domains = ValueUtils.addToValues(domain, old_domains, ',')
    pm.updateValue("""Domains/domains.properties""", "domains", new_domains)

print("RIAVVIARE IL DOMAIN CONTROLLER! \nCAMBIARE UTENTE E PASSWORD NELLA SEZIONE MESSAGING PRIMA DI AVVIARE")