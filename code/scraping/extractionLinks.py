from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import csv

my_url = 'https://www.formula1.com/en/results.html/1952/races.html'
uClient = urlopen(my_url)

page_html = uClient.read()
uClient.close()

page_soup = soup(page_html,"html.parser")
liste_scroll = page_soup.find_all("ul", "resultsarchive-filter ResultFilterScrollable")

url_box = []
for colonne in liste_scroll:
    liste_items = colonne.find_all("li", "resultsarchive-filter-item")
    url = []
    for element in liste_items:
        url.append(element.a["href"])
    url_box.append(url)


#sortie csv
j=0
for i in ["dates" ,"box1" ,"box2"]:
    filename = i + ".csv"
    out = csv.writer(open(filename,"w"), delimiter=',',quoting=csv.QUOTE_ALL)
    out.writerow(url_box[j])
    j+=1
