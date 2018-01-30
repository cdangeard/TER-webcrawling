#parser BeautifulSoup4
from bs4 import BeautifulSoup as soup
#librairie d'acces web par url
from urllib.request import urlopen
#librairie pour l'export en csv
import csv

#récupération de l'url
my_url = 'https://www.formula1.com/en/results.html/1960/races.html'
#ouverture d'un client url
uClient = urlopen(my_url)
#stockage du code html de la page
page_html = uClient.read()
#fermerture du client
uClient.close()

page_soup = soup(page_html,"html.parser")
temp = page_soup.td.next.next.next.next.next.next.next.next.get_text()
print(temp)
