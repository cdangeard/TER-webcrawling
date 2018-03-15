#parser BeautifulSoup4
from bs4 import BeautifulSoup as soup
#librairie d'acces web par url
from urllib.request import urlopen
#librairie pour l'export en csv
import csv
from tableExtract import raceExtract,raceinfoExtract, driversExtract, allraceExtract
from linkExtract import yearUrlExtract, raceUrlExtract
print(raceinfoExtract('https://www.formula1.com/en/results.html/1961/races/189/netherlands.html'))
