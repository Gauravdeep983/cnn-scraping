from bs4 import BeautifulSoup
import requests

base_url = 'https://money.cnn.com/data/hotstocks/'
page = requests.get(base_url)

soup = BeautifulSoup(page.content, 'html.parser')

container = soup.find(id = "wsod_hotStocks")
print(container.prettify())