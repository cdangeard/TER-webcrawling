#librairie pour les requetes SQL
import pymysql
#librairie pour l'export en csv
import csv
#pour la gestion des dates
import datetime

#connection a PHP my admin
connection = pymysql.connect(host='pedago.univ-rennes2.fr',
                             user='',
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

#fonction qui permet de sortir l'attribut gDate sous forme de Datetime
def gDate(date):
    mois = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06", "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}
    return datetime.datetime(int(date[-4:]), int(mois[date[3:6]]), int(date[0:2]), 0, 0, 0)

#fonction qui permet de mettre en forme les identifiants des grands prix sous la forme 'YYYYNN' année/rank
def gpID(rseason, grank):
    gpid = rseason + grank
    if len(gpid)<6:
        gpid = str(rseason)+str(0)+ str(grank)
    return str(gpid)

#fonction qui permet de gérer le NC qui apparait dans le CSV en le transformant en NULL par défaut
def sPos(chaine):
    if chaine == 'NC':
        return 'DEFAULT'
    else:
        return "'"+chaine+"'"

#fonction qui permet de gérer les chaines vides du CSV
def sInc(chaine):
    if chaine == '':
        return 'DEFAULT'
    else:
        return "'"+chaine+"'"

# fonction qui permet de retourner que chaine de caractères en majuscules et sans apostrophes pour respecter les noms deja présents dans la BD
def gName(chaine):
    chaine = chaine.replace("'"," ")
    chaine = chaine.upper()
    return chaine

#ajout des polites de l'année
#Je n'ai pas réussi à faire marche l'IA
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

#ajout des nouvelles teams dans la BD
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

#ajout des nouvelles lignes de la table racedriver
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

#ajout des nouveaux circuits
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

#les GP sont dans l'ordre ou ils se déroulent dans l'année, on a donc facilement leurs rangs
def ajout_grandprix(CSV_grandprix):
    grank = 0
    with connection.cursor()as cursor:
        for ligne in csv.reader(CSV_grandprix, delimiter=","):
            grank += 1
            gpid = gpID(ligne[1][-4:], str(grank))
            name_country = ligne[2].split(',')
            sql = "SELECT circuitID FROM circuit WHERE cName =" + "'" + name_country[0] + "'"
            cursor.execute(sql)
            result = cursor.fetchone()
            circuitID = result['circuitID']
            ajout = "INSERT INTO grandprix VALUES ('"+gpid+"', "+"'"+ gName(ligne[0]) +"'" +", '"+ str(circuitID) + "', '"+ str(gDate(ligne[1]))+"', '"+ ligne[3] +"', '"+str(grank)+"')"
            cursor.execute(ajout)
            connection.commit()
        connection.close()
    return None

#ajout des nouvelles lignes de la table standings
def ajout_standings(CSV_standing):
    rSeason = str(2003) #achanger
    with connection.cursor()as cursor:
        for ligne in csv.reader(CSV_standing, delimiter=","):
            sql = "SELECT driverID FROM racedriver WHERE rDriverNb ='"+ligne[0]+"' AND rSeason='"+str(rSeason)+"'"
            cursor.execute(sql)
            result = cursor.fetchone()
            driverID = result['driverID']
            ajout = "INSERT INTO standings VALUES ('" + str(driverID) + "', '" + gpID(rSeason, str(int(ligne[2])+1)) + "', '"+ ligne[3] +"', " + sPos(ligne[4]) + ", " + sInc(ligne[5]) + ", '" + ligne[6]+ "', '"+ ligne[7] +"')"
            cursor.execute(ajout)
            connection.commit()
        connection.close()
    return None

####### ajout dans la BD  #######
#ajout_driver(fp_racedriver)
#ajout_team(fp_racedriver)
#ajout_racedriver(fp_racedriver)
#ajout_circuit(fp_grandprix)
#ajout_grandprix(fp_grandprix)
#ajout_standings(fp_standing)

####### test des fonctions  #######
#print(gDate("06 Apr 2003"))
#print(ID('driver'))
#print(gName("hhhhhhh'hh"))