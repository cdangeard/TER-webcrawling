#parser BeautifulSoup4
from bs4 import BeautifulSoup as soup
#librairie d'acces web par url
from urllib.request import urlopen
#librairie pour l'export en csv
import csv
from tableExtract import raceExtract,raceinfoExtract, driversExtract, allraceExtract, practiceExtract
from linkExtract import yearUrlExtract, raceUrlExtract, practiceUrl

def sortiecvsUrl(table, url):
    filename = 'cvs/' + url.replace(".html","").replace("https://www.formula1.com/","").replace("/","-") + ".csv"
    out = csv.writer(open(filename,"w"), delimiter=',',quoting=csv.QUOTE_ALL)
    for colonne in table:
        out.writerow(colonne)
    return None

def sortiecvsTable(table, name):
    filename = name+".csv"
    out = csv.writer(open(filename,"w"), delimiter=',',quoting=csv.QUOTE_ALL)
    for colonne in table:
        out.writerow(colonne)
    return None
#sortiecvs(practiceExtract('https://www.formula1.com/en/results.html/1996/races/638/australia/practice-2.html'),'https://www.formula1.com/en/results.html/1996/races/638/australia/practice-2.html')
