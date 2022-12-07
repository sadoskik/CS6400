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
    INSERT INTO hosts(id,hostname,hardware_laptop,
    hardware_corecount,software_os,software_virtualized, iddepartment)
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
    hostSkeleton = "({idhost}, '{hostname}', {hardLap}, {hardCore}, '{softOS}', {softVirt}, {iddepartment})"
    for id in range(1, 1000):
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
            hardCore=hardCore, softOS=softOS, softVirt=softVirt, iddepartment=randint(1,8))
        insertCommand += ",\n"
    insertCommand = insertCommand[:-2]
    print(insertCommand)
    with connection.cursor() as cursor:
        cursor.execute(insertCommand)
        connection.commit()
def fillVuln():
    
    vulnSkeleton = "({id}, '{CVE}', {description})"
    id = 1000
    with open("cve.txt", "r", encoding="utf-8") as fp:
        lines = fp.readlines()
        for line in lines:
            insertCommand = """
                INSERT INTO VULNs(idVULN,CVE,
                description)
                VALUES
                (%s, %s, %s)
                """
            CVE = line.split("\t")[0]
            description = line.split("\t")[1]
            #description = description.replace(":", "").replace("\"", "")
            
            id += 1
            with connection.cursor() as cursor:
                cursor.execute(insertCommand, (id, CVE, description))
                connection.commit()
    

def fillVIT():
    for id in range(100, 150):
        idHost = randint(2000,2999)
        idVIT = id
        timestamp = "2022-"+str(randint(1,12))+"-"+str(randint(1,28))+" "+ ":".join([str(randint(0,23)), str(randint(0,59)), str(randint(0,59))])
        severity = randint(1,5)
        idVULN = randint(1000,2000)
        insertCommand = """
                INSERT INTO VITs(idVIT,severity,
                idVULN, timestamp, idhost)
                VALUES
                (%s, %s, %s, %s, %s)
                """
        with connection.cursor() as cursor:
            cursor.execute(insertCommand, (idVIT, severity, idVULN, timestamp, idHost))
            connection.commit()
def fillDepartments():
    return
    for id in range(100, 110):
        insertCommand = """
                INSERT INTO departments(idVIT,severity,
                idVULN, timestamp, idhost)
                VALUES
                (%s, %s, %s, %s, %s)
                """
        with connection.cursor() as cursor:
            cursor.execute(insertCommand, (idVIT, severity,
                           idVULN, timestamp, idHost))
            connection.commit()
def fillAlerts():
    for id in range(1, 110):
        insertCommand = """
                INSERT INTO alerts(id,alert_time,
                short_description, long_description, iddepartment,
                priority, category, state, idhost)
                VALUES
                ("""
        timestamp = "2022-"+str(randint(1, 12))+"-"+str(randint(1, 28))+" " + ":".join(
            [str(randint(0, 23)), str(randint(0, 59)), str(randint(0, 59))])
        insertCommand = insertCommand + ",".join([str(id), "'"+str(timestamp)+"'",
                                                  "'Network intrusion'", "'Long Desc'", str(
                                                      randint(1, 8)),
                                                  str(randint(1, 5)), "'network'", "'unassigned'", str(randint(1, 1000))]) + ")"
        print(insertCommand)
        with connection.cursor() as cursor:
            cursor.execute(insertCommand)
            connection.commit()
fillAlerts()