#librairie pour les requetes SQL
import pymysql
#librairie pour l'export en csv
import csv
#pour la gestion des dates
import datetime

#connection a PHP my admin
connection = pymysql.connect(host='pedago.univ-rennes2.fr',
                             user='21501288',
                             password='',
                             db='Base-21501288-2',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

racedriver = "../../csv/2003-racedriver.csv"
grandprix = "../../csv/2003-grandPrix.csv"
standing = "../../csv/2003-standing.csv"
fp_racedriver = open(racedriver,"r", encoding="utf-8")
fp_grandprix = open(grandprix,"r", encoding="utf-8")
fp_standing = open(standing,"r", encoding="utf-8")

#ajout d'un pilote dans la BD
#petite pb avec l'incrémentaiton automatique du coup j'ai compté les id avec une requête ^^
def ajout_driver (CSV_driver):
    with connection.cursor()as cursor:
        quelid = "SELECT COUNT(*) FROM driver"
        cursor.execute(quelid)
        ID = cursor.fetchall()
        for ligne in csv.reader(CSV_driver, delimiter=","):
            sql= "SELECT driverID FROM driver WHERE dFirstName ="+"'"+ligne[0]+"'"+" AND dLastName="+"'"+ligne[1]+"'"+""
            cursor.execute(sql)
            result = cursor.fetchone()
            if result == None:
                ID[0]['COUNT(*)'] += 1
                ajout = "INSERT INTO driver VALUES ("+str(ID[0]['COUNT(*)'])+",'"+ligne[0]+"', '"+ligne[1]+"', DEFAULT, DEFAULT, DEFAULT, DEFAULT)"
                cursor.execute(ajout)
                connection.commit()
        connection.close()
    return None

#ajout d'une team dans la BD même pb avec l'IA
def ajout_team(CSV_driver):
    with connection.cursor()as cursor:
        quelid = "SELECT COUNT(*) FROM team"
        cursor.execute(quelid)
        ID = cursor.fetchall()
        for ligne in csv.reader(CSV_driver, delimiter=","):
            sql = "SELECT teamID FROM team WHERE tName =" + "'" + ligne[2] + "'" + ""
            cursor.execute(sql)
            result = cursor.fetchone()
            if result == None:
                ID[0]['COUNT(*)'] += 1
                ajout = "INSERT INTO team VALUES (" + str(ID[0]['COUNT(*)']) + ",'" + ligne[2] + "', DEFAULT, DEFAULT)"
                cursor.execute(ajout)
                connection.commit()
        connection.close()
    return None

def ajout_racedriver(CSV_driver):
    with connection.cursor()as cursor:
        for ligne in csv.reader(CSV_driver, delimiter=","):
            driver = "SELECT driverID FROM driver WHERE dFirstName ="+"'"+ligne[0]+"'"+" AND dLastName="+"'"+ligne[1]+"'"+""
            cursor.execute(driver)
            driverID = cursor.fetchall()
            team = "SELECT teamID FROM team WHERE tName =" + "'" + ligne[2] + "'" + ""
            cursor.execute(team)
            teamID = cursor.fetchall()
            ajout = "INSERT INTO racedriver VALUES (" + str(teamID[0]['teamID']) +", "+ str(driverID[0]['driverID']) +", " + ligne[3]+ ", " + ligne[4]+")"
            cursor.execute(ajout)
            connection.commit()
        connection.close()
    return None

def ajout_circuit(CSV_grandprix):
    with connection.cursor()as cursor:
        quelid = "SELECT COUNT(*) FROM circuit"
        cursor.execute(quelid)
        ID = cursor.fetchall()
        for ligne in csv.reader(CSV_grandprix, delimiter=","):
            name_country = ligne[2].split(',') #sépare les pays et les noms de circuits séparés par une ,
            sql = "SELECT circuitID FROM circuit WHERE cName =" + "'" + name_country[0] + "'"
            cursor.execute(sql)
            result = cursor.fetchone()
            if result == None:
                ID[0]['COUNT(*)'] += 1
                ajout = "INSERT INTO circuit VALUES (" + str(ID[0]['COUNT(*)']) + ",'" + name_country[0] + "', DEFAULT," +"'"+ name_country[1] +"', DEFAULT, DEFAULT, DEFAULT, DEFAULT)"
                cursor.execute(ajout)
                connection.commit()
        connection.close()
    return None

def conversion_date(date):
    mois = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06", "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}
    return datetime.datetime(int(date[-4:]), int(mois[date[3:6]]), int(date[0:2]), 0, 0, 0)

#les GP sont dans l'ordre ou ils se déroulent dans l'année, on a donc le rang
def ajout_grandprix(CSV_grandprix):
    grank = 0
    with connection.cursor()as cursor:
        for ligne in csv.reader(CSV_grandprix, delimiter=","):
            grank += 1
            gpID = ligne[1][-4:] + str(grank)
            if len(gpID)<6:
                gpID = ligne[1][-4:] + str(0) + str(grank)
            name_country = ligne[2].split(',')
            sql = "SELECT circuitID FROM circuit WHERE cName =" + "'" + name_country[0] + "'"
            cursor.execute(sql)
            result = cursor.fetchone()
            circuitID = result['circuitID']
            ajout = "INSERT INTO grandprix VALUES ('"+gpID+"', "+"'"+ ligne[0].replace("'"," ")+"'" +", '"+ str(circuitID) + "', '"+ str(conversion_date(ligne[1]))+"', '"+ ligne[3] +"', '"+str(grank)+"')"
            print(ajout)
            cursor.execute(ajout)
            connection.commit()
        connection.close()
    return None

def ajout_standings(CSV_standing):
    rSeason = 2003 #achanger
    with connection.cursor()as cursor:
        for ligne in csv.reader(CSV_standing, delimiter=","):
            sql = "SELECT teamID, driverID FROM racedriver WHERE rDriverNb ='"+ligne[0]+"' AND rSeason='"+str(rSeason)+"'"
            cursor.execute(sql)
            result = cursor.fetchone()
            teamID = result['teamID']
            driverID = result['driverID']
            ajout = "INSERT INTO grandprix VALUES ('"+str(driverID)+ "', '" +str(teamID) + "', '"+ ligne[2]+"')"
            print(ajout)

#ajout_driver(fp_racedriver)
#ajout_team(fp_racedriver)
#ajout_racedriver(fp_racedriver)
#ajout_circuit(fp_grandprix)
#ajout_grandprix(fp_grandprix)
#print(conversion_date("06 Apr 2003"))
#ajout_standings(fp_standing)
