import pymysql

#test de lecture dans une table MySQL
#tables et leurs attributs
circuit = ["circuitID", "cName", "cCity", "cCountry", "cLength", "cLapRec", "cDriveRec", "cYearRec"]
driver = ["driverID", "dFirstName", "dLastName", "dBirthdate", "dDeathdate", "dCountry", "dGenre"]
grandprix = ["gpID", "gName", "circuitID", "gDate", "gLaps", "gRank"]
racedriver = ["teamID", "driverID", "rSeason", "rDriverNb"]
standings = ["driverID","gpID", "sGrid", "sPos", "sInc", "sPoints", "sLaps"]
team = ["teamID", "tName", "tCountry", "tWas"]
testdriver = ["teamID", "driverID", "tSeason"]

#connection a PHP my admin
connection = pymysql.connect(host='pedago.univ-rennes2.fr',
                             user='21501288',
                             password='',
                             db='Base-21501288-2',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)
try:
    with connection.cursor()as cursor:
        sql="SELECT dFirstName, driverID FROM driver"  # --> lecture des pilotes et des identifiants dans la BD
        cursor.execute(sql)
        result = cursor.fetchall()
        count = cursor.rowcount #compte le nombre de lignes affectées par la requete
        print(result)
        print(count)
finally:
    connection.close()
