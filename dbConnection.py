from getpass import getpass
from mysql.connector import connect, Error
from random import randint
import random
import string

try:
    connection = connect(
        host="localhost",
        user="root",
        password="root",
        database="SIEM",
    )
    print(connection)

except Error as e:
    print(e)

def fillHosts():
    insertCommand = """
    INSERT INTO hosts(idhosts,hostname,hardware_laptop,
    hardware_corecount,software_os,software_virtualized)
    VALUES

    """
    OS_list = ["High Sierra(macOS 10.13)",
        "Mojave(macOS 10.14)",
        "Catalina(macOS 10.15)",
        "Big Sur(macOS 11)",
        "Windows 7",
        "Windows 8",
        "Windows 10",
        "Windows 11",
        "Ubuntu",
        "LinuxMint",
        "Debian",
        "Arch",
        "CentOS"]
    hostSkeleton = "({idhost}, '{hostname}', {hardLap}, {hardCore}, '{softOS}', {softVirt})"
    for id in range(2050, 4000):
        hardLap = randint(1,2) == 1
        if(hardLap):
            hostname = "LAPTOP-"
        else:
            hostname = "DESKTOP-"
        hostname += ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        hardCore = 2**randint(2,6)
        softOS = random.choice(OS_list)
        softVirt = randint(1,2) == 1
        insertCommand += hostSkeleton.format(idhost=id, hostname=hostname, hardLap=hardLap, 
            hardCore=hardCore, softOS=softOS, softVirt=softVirt)
        insertCommand += ",\n"
    insertCommand = insertCommand[:-2]
    print(insertCommand)
    with connection.cursor() as cursor:
        cursor.execute(insertCommand)
        connection.commit()
def fillVuln():
    insertCommand = """
    INSERT INTO VULNs(idVULN,CVE,
    description)
    VALUES

    """
    vulnSkeleton = "({id}, '{CVE}', {description})"
    id = 1000
    with open("cve.txt", "r") as fp:
        lines = fp.readlines()
        for line in lines:
            CVE = line.split("\t")[0]
            description = line.split("\t")[1]
            description.replace
            insertCommand += vulnSkeleton.format(id=id, CVE=CVE, description=description)
            insertCommand += ",\n"
            id += 1
    insertCommand = insertCommand[:-2]
    with connection.cursor() as cursor:
        cursor.execute(insertCommand)
        connection.commit()

def fillVIT():
    for id in range(100, 150):
        pass
fillVuln()