#parser BeautifulSoup4
from bs4 import BeautifulSoup as soup
#librairie d'acces web par url
from urllib.request import urlopen
#librairie pour l'export en csv
import csv

def yearUrlExtract(url):
    #ouverture d'un client url
    uClient = urlopen(url)
    #stockage du code html de la page
    page_html = uClient.read()
    #fermerture du client
    uClient.close()
    page_soup = soup(page_html,"html.parser")
    liste_urls = []
    liste_scroll = page_soup.find_all("ul", "resultsarchive-filter ResultFilterScrollable")
    listeYear = liste_scroll[0].find_all("li", "resultsarchive-filter-item")
    for year in listeYear:
        liste_urls.append('https://www.formula1.com' + year.a["href"])
    return liste_urls


def raceUrlExtract(url):
    #ouverture d'un client url
    uClient = urlopen(url)
    #stockage du code html de la page
    page_html = uClient.read()
    #fermerture du client
    uClient.close()
    page_soup = soup(page_html,"html.parser")
    liste_urls = []
    liste_scroll = page_soup.find_all("ul", "resultsarchive-filter ResultFilterScrollable")
    listeRace = liste_scroll[2].find_all("li", "resultsarchive-filter-item")
    for race in listeRace:
        liste_urls.append('https://www.formula1.com' + race.a["href"])
    return liste_urls
