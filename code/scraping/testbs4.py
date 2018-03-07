#parser BeautifulSoup4
from bs4 import BeautifulSoup as soup
#librairie d'acces web par url
from urllib.request import urlopen
#librairie pour l'export en csv
import csv

#récupération de l'url
my_url = 'https://www.formula1.com/en/results.html/1950/drivers/94/great-britain/race-result.html'
#ouverture d'un client url
uClient = urlopen(my_url)
#stockage du code html de la page
page_html = uClient.read()
#fermerture du client
uClient.close()

#transforme la page html, dans un format propre au parser, qui permet ensuite d'extraire les informations voulus
page_soup = soup(page_html,"html.parser")
#page_soup.h1 #renvoie l'integralité des
#find_all() ou findAll() fait le meme effet, mais rend une liste des occurences (utilisation recomandé pour futurs traitement)

temp = page_soup.findAll('tr')
print(temp[1].find("a","grey").text)
