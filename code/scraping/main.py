#parser BeautifulSoup4
from bs4 import BeautifulSoup as soup
#librairie d'acces web par url
from urllib.request import urlopen
#librairie pour l'export en csv
import csv
import pprint
import numpy as np #pour manipuler les taleaux facilement
from tableExtract import raceExtract,raceinfoExtract, driversExtract, allraceExtract, practiceExtract, gridExtract
from linkExtract import yearUrlExtract, raceUrlExtract, practiceUrl
from cvsExtract import sortiecvsTable, sortiecvsUrl

url = 'https://www.formula1.com/en/results.html'
url2 = 'https://www.formula1.com/en/results.html/2003/races/737/australia.html'
url3 = 'https://www.formula1.com/en/results.html/1951/races.html'

#recupere l'année dans un url
def urlIntoYear(url):
    pos = url.find('html')
    return url[pos+5:pos+9]

#renverse une table (transposé matricielle, ou inversion de l'ordre des indices fonctionne pour une liste de listes)
def renverse(table):
    return np.array(table).transpose().tolist()

#affiche sur le terminal, la totalité des extractions des differentes pages
#execution tres longue
def boucleAffiche(url):
    liste_dates = yearUrlExtract(url)
    print(liste_dates)
    for annee in liste_dates:
        print('\n\n ########'+annee+'######## \n\n')
        print('\n #####race###### \n')
        print(allraceExtract(annee))
        driver = annee.replace('races','drivers')
        print('\n #####'+driver+'###### \n')
        print(driversExtract(driver))
        liste_courses = raceUrlExtract(annee)
        print(liste_courses)
        for course in liste_courses:
            print('\n #####'+course+'#######"" \n')
            print(raceinfoExtract(course))
            print('\n')
            print(raceExtract(course))
            practices = practiceUrl(course)
            print('\n')
            for practice in practices:
                print(practiceExtract(practice))

#resort la position au départ d'un coureur en fonction de son numéro de con
def startingpos(num, grid):
    if grid != []:
        for i in range(0, len(grid[0])):
            if num == grid[1][i]:
                return grid[0][i]
    return ''

#ajoute les données à la table racedriver, pour un coureur
def ajoutDriver(tableprenom, tablenom, tableteam, tablenum, num, prenom, nom, team):
    for i in range(0,len(tableprenom)):
        if (nom == tablenom[i] and prenom == tableprenom[i]):
            return [tableprenom, tablenom, tableteam, tablenum, i]
    return [tableprenom + [prenom], tablenom + [nom], tableteam + [team], tablenum+ [num], len(tableprenom)+1]#len(tableDriver[0])-1,

#ajoute les données à la table standing, pour un coureur
def ajoutStanding(tsidDriver, tsteamName, tsidGp, tsGrid, tsPos, tsInc, tsPoints, tsLaps, tableRace, tableGrid, gid):
    sidDriver = tableRace[1]
    steamName = tableRace[4]
    sPos = tableRace[0]
    sPoints = tableRace[7]
    sLaps = tableRace[5]
    if tableRace[6] == 'DNF':
        sInc = 'DNF'
    else:
        sInc = ''
    sGrid = startingpos(tableRace[1], tableGrid)
    return [tsidDriver + [sidDriver], tsteamName + [steamName], tsidGp + [gid], tsGrid + [sGrid], tsPos + [sPos], tsInc + [sInc], tsPoints + [sPoints], tsLaps + [sLaps]]


#Extrait et transforme les données en vue d'etre integrer dans la BDD, les tableaux en sortie sont au meme format que dans sortieCSVOneyear
#seulement ce sont des listes de listes pyton
def ShapeOneYear(url):
    DriverNom = DriverPrenom = teamName = rSeason = rDrivernb = []
    #racedriver = [DriverPrenom, DriverNom, teamName, rSeason, rDrivernb]
    sidDriver = steamName = sidGp = sGrid = sPos = sInc = sPoints = sLaps = []
    #standing = [sidDriver, steamName, sidGp, sGrid, sPos, sInc, sPoints, sLaps]
    gnom = gcircuit = gdate = glaps = []
    #grandPrix = [gnom, gcircuit, gdate, glaps]
    liste_courses = raceUrlExtract(url)
    gid = 0
    grandPrix = []
    for course in liste_courses:
        print(course)
        season = urlIntoYear(url)
        #infos sur le grand grix
        grandPrix.append(raceinfoExtract(course))

        #drivers present sur le circuit
        race = raceExtract(course)#0.pos, 1.no, 2.prenom, 3.nom, 4.team,5.laps, 6.time ,7.pts
        grid = gridExtract(course)#pos , no
        raceinv = renverse(race)#plus facile à manipuler
        #
        for i in range(0, len(race[0])):
            [DriverPrenom, DriverNom, teamName, rDrivernb, idDri] = ajoutDriver(DriverPrenom, DriverNom, teamName, rDrivernb, raceinv[i][1], raceinv[i][2], raceinv[i][3], raceinv[i][4])
            [sidDriver, steamName, sidGp, sGrid, sPos, sInc, sPoints, sLaps] = ajoutStanding(sidDriver, steamName, sidGp, sGrid, sPos, sInc, sPoints, sLaps , raceinv[i], grid, gid)
        gid = gid + 1
    rSeason = [urlIntoYear(url)]*len(DriverPrenom)
    racedriver = [DriverPrenom, DriverNom, teamName, rSeason, rDrivernb]
    standing = [sidDriver, steamName, sidGp, sGrid, sPos, sInc, sPoints, sLaps]
    return racedriver, grandPrix, standing

#sort trois tableaux csv contenant les infos extrait du site pour une année
#en entrée, l'url de la page principale de l'année en question
#en sortie:
#le tableau racedriver, contenant par colonne dans cet ordre: [DriverPrenom, DriverNom, teamName, rSeason, rDrivernb]
#le tableau standing , contenant par colonne dans cet ordre: [sidDriver, steamName, sidGp, sGrid, sPos, sInc, sPoints, sLaps]
# avec sidGp le numéro python (de 0 à n-1) du grandPrix dans le tableau suivant
#le tableau Gp , contenant par colonne dans cet ordre:[gnom, gcircuit, gdate, glaps]
#gcircuit n'est pas encore mis en forme totalement, pour le moment le nom du circuit contient le pays (à revoir en foncition de la norme BDD pour les pays)
def sortieCSVOneyear(url):
    racedriver, grandPrix, standing = ShapeOneYear(url)
    sortiecvsTable(renverse(racedriver),urlIntoYear(url)+'-racedriver')
    sortiecvsTable(grandPrix,urlIntoYear(url)+'-grandPrix')
    sortiecvsTable(renverse(standing),urlIntoYear(url)+'-standing')
    return None

#extrait du site la totalité des tableaux pour toute les années disponible sur le site web
#execution tres longue
def sortieCSVAllyear(url = 'https://www.formula1.com/en/results.html'):
    liste_dates = yearUrlExtract(url)
    for annee in liste_dates:
        sortieCSVOneyear(annee)
    return None


######### MAIN ############

sortieCSVOneyear(url3)
#sortieCSVAllyear()
