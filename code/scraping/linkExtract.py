#parser BeautifulSoup4
from bs4 import BeautifulSoup as soup
#librairie d'acces web par url
from urllib.request import urlopen
#librairie pour l'export en csv
import csv

#retourne un tableau avec la liste des urls de differentes années disponible dans le menu déroulant de gauche
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
    return liste_urls[1:]

#retourne la liste des url des differentes courses disponible dans le menu déroulant de droite
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
    return liste_urls[1:]

#retourne si possible, la liste des urls des courses "practice", disponible dans le sous menu des grand prix
def practiceUrl(url):
    #ouverture d'un client url
    uClient = urlopen(url)
    #stockage du code html de la page
    page_html = uClient.read()
    #fermerture du client
    uClient.close()
    page_soup = soup(page_html,"html.parser")
    liste_urls = []
    liste_scroll = page_soup.find_all("li","side-nav-item")
    liste_practice = []
    for it in liste_scroll[1:]:
        if it.a["data-value"][:8] == 'practice':
            liste_practice.append('https://www.formula1.com' + it.a["href"])
    return liste_practice
