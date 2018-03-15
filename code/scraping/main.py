#parser BeautifulSoup4
from bs4 import BeautifulSoup as soup
#librairie d'acces web par url
from urllib.request import urlopen
#librairie pour l'export en csv
import csv
from tableExtract import raceExtract,raceinfoExtract, driversExtract, allraceExtract, practiceExtract
from linkExtract import yearUrlExtract, raceUrlExtract, practiceUrl

#print(practiceUrl('https://www.formula1.com/en/results.html/1959/races/170/indianapolis-500.html'))
#print(raceExtract('https://www.formula1.com/en/results.html/1959/races/170/indianapolis-500.html'))
print(practiceUrl('https://www.formula1.com/en/results.html/1996/races/638/australia/practice-2.html'))
