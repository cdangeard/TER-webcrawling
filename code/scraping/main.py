#parser BeautifulSoup4
from bs4 import BeautifulSoup as soup
#librairie d'acces web par url
from urllib.request import urlopen
#librairie pour l'export en csv
import csv
from tableExtract import raceExtract,raceinfoExtract, driversExtract, allraceExtract, practiceExtract, gridExtract
from linkExtract import yearUrlExtract, raceUrlExtract, practiceUrl
from cvsExtract import sortiecvsTable, sortiecvsUrl

url = 'https://www.formula1.com/en/results.html'
url2 = 'https://www.formula1.com/en/results.html/2003/races/737/australia.html'
url3 = 'https://www.formula1.com/en/results.html/2006/races/737/australia/race-result.html'

def urlIntoYear(url):
    pos = url.find('html')
    return url[pos+5:pos+9]

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
            



        #ydriver = driversExtract(annee.replace('races','drivers'))
        #DriverPrenom.append(ydriver[0])
        #DriverNom.append(ydriver[1])
        #nat.append(ydriver[2])
        #teamName.append(ydriver[3])
        #rSeason = [urlIntoYear(url)]*len(ydriver[0])
    print()
    return racedriver


sortiecvsTable(AllShape(url),'racedriver')
#print(gridExtract('https://www.formula1.com/en/results.html/2006/races/791/malaysia.html'))
#boucleAffiche(url)
#driverShaping(url3,999)
