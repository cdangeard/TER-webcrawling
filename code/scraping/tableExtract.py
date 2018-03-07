#parser BeautifulSoup4
from bs4 import BeautifulSoup as soup
#librairie d'acces web par url
from urllib.request import urlopen
#librairie pour l'export en csv
import csv



#retourne le tableau sous forme d'un array si csv est faux, sinon ne retourne rien mais export le tableau au format csv
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
    if csvreturn:
        filename = my_url.replace(".html","").replace("https://www.formula1.com/","").replace("/","-") + ".csv"
        out = csv.writer(open(filename,"w"), delimiter=',',quoting=csv.QUOTE_ALL)
        for colonne in tableau:
            out.writerow(colonne)
        return None
    return tableau

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
    return [titre, date, circuit]


def raceExtract(url, csvreturn = False):
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
    tableau = [pos, no, prenoms, noms, cars]

    for ligne in temp[1:]:
        pos.append(ligne.find('td', "dark"))
        no.append(ligne.find('td', "dark hide-for-mobile").text)
        prenoms.append(ligne.find('span',"hide-for-tablet").text)
        noms.append(ligne.find('span',"hide-for-mobile").text)
        cars.append(ligne.find("td", "semi-bold uppercase hide-for-tablet").text)
    if csvreturn:
        filename = my_url.replace(".html","").replace("https://www.formula1.com/","").replace("/","-") + ".csv"
        out = csv.writer(open(filename,"w"), delimiter=',',quoting=csv.QUOTE_ALL)
        for colonne in tableau:
            out.writerow(colonne)
        return None
    return tableau

def driversExtract(url, csvreturn = False):
    #ouverture d'un client url
    uClient = urlopen(url)
    #stockage du code html de la page
    page_html = uClient.read()
    #fermerture du client
    uClient.close()
    page_soup = soup(page_html,"html.parser")
    temp = page_soup.findAll('tr')

    pos = []
    prenoms = []
    noms = []
    nationality = []
    car = []
    points = []
    tableau = [pos, prenoms, noms,nationality, car]

    for ligne in temp[1:]:
        pos.append(ligne.find('td', "dark").text)
        prenoms.append(ligne.find('span',"hide-for-tablet").text)
        noms.append(ligne.find('span',"hide-for-mobile").text)
        nationality.append(ligne.find("td", "dark semi-bold uppercase").text)
        car.append(ligne.find("a","grey").text)
    if csvreturn:
        filename = my_url.replace(".html","").replace("https://www.formula1.com/","").replace("/","-") + ".csv"
        out = csv.writer(open(filename,"w"), delimiter=',',quoting=csv.QUOTE_ALL)
        for colonne in tableau:
            out.writerow(colonne)
        return None
    return tableau
