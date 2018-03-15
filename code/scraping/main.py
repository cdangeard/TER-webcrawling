#parser BeautifulSoup4
from bs4 import BeautifulSoup as soup
#librairie d'acces web par url
from urllib.request import urlopen
#librairie pour l'export en csv
import csv
from tableExtract import raceExtract,raceinfoExtract, driversExtract, allraceExtract, practiceExtract
from linkExtract import yearUrlExtract, raceUrlExtract, practiceUrl
from cvsExtract import sortiecvs


url = 'https://www.formula1.com/en/results.html'
liste_dates = yearUrlExtract(url)
print(liste_dates)

for annee in liste_dates[1:]:
    print('\n\n ########'+annee+'######## \n\n')
    print('\n #####race###### \n')
    print(allraceExtract(annee))
    driver = annee.replace('races','drivers')
    print('\n #####'+driver+'###### \n')
    print(driversExtract(driver))
    liste_courses = raceUrlExtract(annee)
    print(liste_courses)
    for course in liste_courses[1:]:
        print('\n #####'+course+'#######"" \n')
        print(raceinfoExtract(course))
        print('\n')
        print(raceExtract(course))
        practices = practiceUrl(course)
        print('\n')
        for practice in practices:
            print(practiceExtract(practice))
