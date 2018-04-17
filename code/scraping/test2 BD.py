import pymysql
#connection a PHP my admin
connection = pymysql.connect(host='pedago.univ-rennes2.fr',
                             user='21501288',
                             password='FAf0WM7hz9xuIqp0Zdqs',
                             db='Base-21501288-2',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor()as cursor:
        #rajoute une ligne de ligne dans la table driver
        sql="INSERT INTO driver ('dFirstName', 'dLastName', 'dBirthdate', 'dDeathdate', 'dCountry', 'dGenre') VALUES ('Jessica', 'Coulon', DEFAULT, DEFAULT, DEFAULT, DEFAULT)"
        cursor.execute(sql)
        connection.commit()

#retour arrière si erreur
except:
    connection.rollback()

finally:
    connection.close()