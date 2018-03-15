#parser BeautifulSoup4
from bs4 import BeautifulSoup as soup
#librairie d'acces web par url
from urllib.request import urlopen
#librairie pour l'export en csv
import csv
from tableExtract import raceExtract,raceinfoExtract, driversExtract, allraceExtract, practiceExtract
from linkExtract import yearUrlExtract, raceUrlExtract, practiceUrl

def sortiecvs(table, url):
    filename = url.replace(".html","").replace("https://www.formula1.com/","").replace("/","-") + ".csv"
    out = csv.writer(open('cvs/' + filename,"w"), delimiter=',',quoting=csv.QUOTE_ALL)
    for colonne in table:
        out.writerow(colonne)
    return None
