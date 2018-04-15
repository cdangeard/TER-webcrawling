#parser BeautifulSoup4
from bs4 import BeautifulSoup as soup
#librairie d'acces web par url
from urllib.request import urlopen
#librairie pour l'export en csv
import csv
import pprint
from tableExtract import raceExtract,raceinfoExtract, driversExtract, allraceExtract, practiceExtract, gridExtract
from linkExtract import yearUrlExtract, raceUrlExtract, practiceUrl
from cvsExtract import sortiecvsTable, sortiecvsUrl

url = 'https://www.formula1.com/en/results.html'
url2 = 'https://www.formula1.com/en/results.html/2003/races/737/australia.html'
url3 = 'https://www.formula1.com/en/results.html/2006/races/792/australia.html'

#recupere l'année dans un url
def urlIntoYear(url):
    pos = url.find('html')
    return url[pos+5:pos+9]

#affiche sur le terminal, la totalité des extractions des differentes pages
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

#extrait et met en forme les données du site en vu d'integration dans la bdd retourne un tableau de tableau de tableau, avec les differents table
#les tableau contenant un id font ref à la position dans un tableau
def AllShape(url):
    liste_dates = yearUrlExtract(url)
    DriverNom = DriverPrenom = []
    driver = [DriverPrenom, DriverNom]
    idDriver = teamName = rSeason = rDrivernb = []
    racedriver = [idDriver, teamName, rSeason, rDrivernb]
    idDriver = teamName = idGp = sGrid = sPos = sInc = sPoints = sLaps = []
    standing = [idDriver, teamName, idGp, sGrid, sPos, sInc, sPoints, sLaps]
    gnom = gcircuit = gdate = glaps = []
    grandPrix = [gnom, gcircuit, gdate, glaps]
    for annee in liste_dates:
        print(annee)
        liste_courses = raceUrlExtract(annee)
        for course in liste_courses:
            print(course)
            raceinfo = raceinfoExtract(course)

def ajoutDriver(tableprenom, tablenom, tableteam, tablenum, prenom, nom, team, num):
    for i in range(0,len(tableprenom)):
        if (nom == tablenom[i] and prenom == tableprenom[i]):
            return [tableprenom, tablenom, tableteam, tablenum, i]
    return [tableprenom + [prenom], tablenom + [nom], tableteam + [team], tablenum+ [num], len(tableprenom)+1]#len(tableDriver[0])-1,

def startingpos(num, sgrid):
    for i in range(0, len(sgrid[0])):
        if num == sgrid[1][i]:
            return sgrid[0][i]
    return ''


def ShapeOneYear(url):
    DriverNom = DriverPrenom = teamName = rSeason = rDrivernb = []
    #racedriver = [DriverPrenom, DriverNom, teamName, rSeason, rDrivernb]#wtf tiens pas compte des modifs?
    sidDriver = steamName = sidGp = sGrid = sPos = sInc = sPoints = sLaps = []
    #standing = [sidDriver, steamName, sidGp, sGrid, sPos, sInc, sPoints, sLaps]
    gnom = gcircuit = gdate = glaps = []
    #grandPrix = [gnom, gcircuit, gdate, glaps]
    liste_courses = raceUrlExtract(url)
    gid = 0
    grandPrix = []
    for course in liste_courses[0:3]:
        print(course)
        season = urlIntoYear(url)
        #infos sur le grand grix
        grandPrix.append(raceinfoExtract(course))
        #gnom += [raceinfo[0]]
        #gdate += [raceinfo[1]]
        #gcircuit += [raceinfo[2]]
        #glaps += [raceinfo[3]]

        #drivers present sur le circuit
        race = raceExtract(course)#0.pos, 1.no, 2.prenom, 3.nom, 4.team,5.laps, 6.time ,7.pts
        grid = gridExtract(course)#pos , no
        for i in range(0, len(race[0])):
            [DriverPrenom, DriverNom, teamName, rDrivernb, idDri] = ajoutDriver(DriverPrenom, DriverNom, teamName, rDrivernb, race[2][i], race[3][i], race[4][i], race[1][i])
            steamName.append(race[4][i])
            sidGp.append(gid)
            sPos.append(race[0][i])
            sPoints.append(race[7][i])
            sLaps.append(race[5][i])
            if race[6][i] == 'DNF':
                sInc.append('DNF')
            else:
                sInc.append('')
            sGrid.append(startingpos(race[0][i], grid))

            #sGrid
            sGrid.append(grid[0][i])
        gid = gid + 1


    rSeason = [urlIntoYear(url)]*len(DriverPrenom)
    racedriver = [DriverPrenom, DriverNom, teamName, rSeason, rDrivernb]
    #grandPrix = [gnom, gcircuit, gdate, glaps]
    standing = [sidDriver, steamName, sidGp, sGrid, sPos, sInc, sPoints, sLaps]
    #print(standing)
    print(grandPrix)


        #print(racedriver[0])
        #for i in range(grid[0]):
            #
        #ydriver = driversExtract(annee.replace('races','drivers'))
        #DriverPrenom.append(ydriver[0])
        #DriverNom.append(ydriver[1])
        #nat.append(ydriver[2])
        #teamName.append(ydriver[3])

    return racedriver, grandPrix, standing

racedriver, grandPrix, standing = ShapeOneYear(url2)
sortiecvsTable(racedriver,urlIntoYear(url2)+'-racedriver')
sortiecvsTable(grandPrix,urlIntoYear(url2)+'-grandPrix')
sortiecvsTable(standing,urlIntoYear(url2)+'-standing')
#sortiecvsTable(AllShape(url),'racedriver')

######### MAIN ############
#sortiecvsTable(AllShape(url),'racedriver')

#print(gridExtract('https://www.formula1.com/en/results.html/2006/races/791/malaysia.html'))
#boucleAffiche(url)
#driverShaping(url3,999)
