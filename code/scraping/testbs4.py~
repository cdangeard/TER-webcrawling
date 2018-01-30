from bs4 import BeautifulSoup as soup
from urllib import urlopen

my_url = 'https://www.formula1.com/en/results.html/1950/races/94/great-britain/race-result.html'
uClient = urlopen(my_url)

page_html = uClient.read()
uClient.close()

page_soup = soup(page_html,"html.parser")
print(page_soup.h1)
