#parser BeautifulSoup4
from bs4 import BeautifulSoup as soup
#librairie d'acces web par url
from urllib.request import urlopen
#librairie pour l'export en csv
import csv
from tableExtract import raceExtract,raceinfoExtract, driversExtract, allraceExtract, practiceExtract
from linkExtract import yearUrlExtract, raceUrlExtract, practiceUrl

#sort un tableau de tableau au format csv, en adaptant un url en nom de fichier
def sortiecvsUrl(table, url):
    filename = 'csv/' + url.replace(".html","").replace("https://www.formula1.com/","").replace("/","-") + ".csv"
    out = csv.writer(open(filename,"w"), delimiter=',',quoting=csv.QUOTE_ALL)
    for colonne in table:
        out.writerow(colonne)
    return None

#sort un tableau de tableau au format csv, dont le nom est donné
def sortiecvsTable(table, name):
    filename = "csv/" + name + ".csv"
    with open(filename,'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(table)
    return None
