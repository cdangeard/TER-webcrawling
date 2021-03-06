#parser BeautifulSoup4
from bs4 import BeautifulSoup as soup
#librairie d'acces web par url
from urllib.request import urlopen
#librairie pour l'export en csv
import csv

#retourne le tableau sous forme d'un array si csv est faux, sinon ne retourne rien mais export le tableau au format csv
#retourne les infos de la page race + all:  dates, grand prix, prenoms et nom du vainceur , equipes nombre de tours, et temps
def allraceExtract(url, csvreturn = False):
    #ouverture d'un client url
    uClient = urlopen(url)
    #stockage du code html de la page
    page_html = uClient.read()
    #fermerture du client
    uClient.close()
    page_soup = soup(page_html,"html.parser")
    temp = page_soup.findAll('tr')

    dates = []
    pays = []
    prenoms = []
    noms = []
    cars = []
    laps = []
    time = []
    tableau = [dates, pays, prenoms, noms, cars, laps, time]

    for ligne in temp[1:]:
        dates.append(ligne.a.text.replace(" ","").replace("\n",""))
        pays.append(ligne.find('td', "dark hide-for-mobile").text)
        prenoms.append(ligne.find('span',"hide-for-tablet").text)
        noms.append(ligne.find('span',"hide-for-mobile").text)
        cars.append(ligne.find("td", "semi-bold uppercase ").text)
        laps.append(ligne.find("td", "bold hide-for-mobile").text)
        time.append(ligne.find("td", "dark bold hide-for-tablet").text)
    return tableau

#retourne les infos sur un course (titre, date, et nom du circuit)
def raceinfoExtract(url):
    uClient = urlopen(url)
    #stockage du code html de la page
    page_html = uClient.read()
    #fermerture du client
    uClient.close()
    page_soup = soup(page_html,"html.parser")
    titre = page_soup.h1.text.replace("  ","").replace("\n","").replace(" - RACE RESULT","")[5:]
    date = page_soup.find("p", "date").find("span","full-date").text
    circuit = page_soup.find("p", "date").find("span","circuit-info").text
    laps = page_soup.findAll("tr")[1].find("td", "bold hide-for-mobile").text
    return [titre, date, circuit, laps]

#retourne les positions de départ et numero du coureur
def gridExtract(url):
#exrait la position en début du course et le numero des joueurs
    uClient = urlopen(url)
    #stockage du code html de la page
    page_html = uClient.read()
    #fermerture du client
    uClient.close()
    page_soup = soup(page_html,"html.parser")
    liste_scroll = page_soup.find_all("li","side-nav-item")
    for it in liste_scroll[1:]:
        if it.a["data-value"] == 'starting-grid':
            url_practice = ('https://www.formula1.com' + it.a["href"])
            #ouverture d'un client url
            uClient = urlopen(url_practice)
            #stockage du code html de la page
            page_html = uClient.read()
            #fermerture du client
            uClient.close()
            page_soup2 = soup(page_html,"html.parser")
            temp = page_soup2.findAll('tr')

            pos = []
            no = []
            tableau =[pos, no]
            for ligne in temp[1:]:
                darkTruc = ligne.find_all('td', 'dark')
                pos.append(darkTruc[0].text)
                no.append(darkTruc[1].text)
            return tableau
    return []

# retourne, position, numero, nom, prenom, et equipe des coureurs (page races + pays)
def raceExtract(url):
    #ouverture d'un client url
    uClient = urlopen(url)
    #stockage du code html de la page
    page_html = uClient.read()
    #fermerture du client
    uClient.close()
    page_soup = soup(page_html,"html.parser")
    temp = page_soup.findAll('tr')

    pos = []
    no = []
    prenoms = []
    noms = []
    cars = []
    laps = []
    time = []
    pts = []
    tableau = [pos, no, prenoms, noms, cars, laps, time, pts]

    for ligne in temp[1:]:
        pos.append(ligne.find('td', "dark").text)
        no.append(ligne.find('td', "dark hide-for-mobile").text)
        prenoms.append(ligne.find('span',"hide-for-tablet").text)
        noms.append(ligne.find('span',"hide-for-mobile").text)
        cars.append(ligne.find("td", "semi-bold uppercase hide-for-tablet").text)
        laps.append(ligne.find("td", "bold hide-for-mobile").text)
        time.append(ligne.findAll("td", "dark bold")[1].text)
        pts.append(ligne.findAll("td", "bold")[3].text)
    return tableau

#retourne nom prénom, nationalitu (format 3 lettres), et team de la page driver
def driversExtract(url):
    #ouverture d'un client url
    uClient = urlopen(url)
    #stockage du code html de la page
    page_html = uClient.read()
    #fermerture du client
    uClient.close()
    page_soup = soup(page_html,"html.parser")
    temp = page_soup.findAll('tr')

    prenoms = []
    noms = []
    nationality = []
    car = []
    tableau = [prenoms, noms, nationality, car]
    for ligne in temp[1:]:
        prenoms.append(ligne.find('span',"hide-for-tablet").text)
        noms.append(ligne.find('span',"hide-for-mobile").text)
        nationality.append(ligne.find("td", "dark semi-bold uppercase").text)
        car.append(ligne.find("a","grey").text)
    return tableau

#retourne les infos, des differentes pages practices, prenom et nom des coureurs
def practiceExtract(url):
    #ouverture d'un client url
    uClient = urlopen(url)
    #stockage du code html de la page
    page_html = uClient.read()
    #fermerture du client
    uClient.close()
    page_soup = soup(page_html,"html.parser")
    temp = page_soup.findAll('tr')
    prenoms = []
    noms = []
    tableau = [prenoms, noms]
    for ligne in temp[1:]:
        prenoms.append(ligne.find('span',"hide-for-tablet").text)
        noms.append(ligne.find('span',"hide-for-mobile").text)
    return tableau
