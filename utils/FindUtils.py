import os.path

from base import EapManagerException
from utils.Propertymanager import PropertyManager


__author__ = "Samuele Dell'Angelo (Red Hat)"

class FindUtils:

    @staticmethod
    def getCluster(domain):
        singleprops = PropertyManager("Domains/"+domain+".properties")
        clusters = singleprops.getValue("clusters").split(",")
        for i in range(len(clusters)):
            print(str(i)+") "+clusters[i])

        try:
            clus = int(raw_input("numero corrispondente al cluster >"))
        except ValueError:
            raise EapManagerException("ERRORE: Inserire un numero")

        if(clus>len(clusters)):
            raise EapManagerException("ERRORE: Inserire un numero che sia compreso in quelli indicati")
        else:
            return clusters[clus]

    @staticmethod
    def getDomain(basefile):
        domprops = PropertyManager("Domains/"+basefile+".properties")
        domains = domprops.getValue("domains").split(',')
        for i in range(len(domains)):
            print(str(i)+") "+domains[i])

        try:
            dom = int(raw_input("numero corrispondente al dominio >"))
        except ValueError:
            raise EapManagerException("ERRORE: Inserire un numero")

        if(dom>len(domains)):
            raise EapManagerException("ERRORE: Inserire un numero che sia compreso in quelli indicati")
        else:
            return domains[dom]

    @staticmethod
    def getInstance(domain,cluster):
        singleprops = PropertyManager("Domains/"+domain+".properties")
        instances = singleprops.getValue("cluster."+cluster+".instances").split(",")

        for i in range(len(instances)):
            print(str(i)+") "+instances[i])

        try:
            insts = int(raw_input("numero corrispondente all'istanza >"))
        except ValueError:
            raise EapManagerException("ERRORE: Inserire un numero")

        if(insts>len(instances)):
            raise EapManagerException("ERRORE: Inserire un numero che sia compreso in quelli indicati")
        else:
            hostPrefix = singleprops.getValue("host.prefix")
            hostNumb = int(singleprops.getValue("host.number"))
            hostsuffix = singleprops.getValue("host.suffix")

            for i in range(hostNumb):
                propKey="cluster."+cluster+"."+(hostPrefix if hostPrefix != None else "")+str(i+1)+(hostsuffix if hostsuffix != None else "")+"."+"instances"
                if (str(singleprops.getValue(propKey)) == instances[insts]):
                    host = hostPrefix+str(i+1)
                    print(host)
                    return (instances[insts],host)

            raise EapManagerException("ERRORE istanza non deifinita nella configurazione")


    @staticmethod
    def getHostPrefix(domain):
        singleprops = PropertyManager("Domains/"+domain+".properties")
        return singleprops.getValue("host.prefix")

    @staticmethod
    def findPath():
        try:
            path = str(raw_input("inserire il path assoluto del file >"))
            path.strip()
            if(os.path.isfile(path) != True or ((path.find("war") == -1) and (path.find("ear") == -1))):
                raise EapManagerException("ERRORE: il percorso non punta a un file valido")

            name = str(raw_input("inserire il nome dell'applicazione >"))

            return (path,name)

        except ValueError:
            raise EapManagerException("ERRORE: Inserire una stringa")

    @staticmethod
    def getGenericString(prompt):
        try:

            name = str(raw_input(prompt))

            return name

        except ValueError:
            raise EapManagerException("ERRORE: Inserire una stringa")


