from bs4 import BeautifulSoup
import requests

# Hotstocks page
def hotstocks():
    base_url = 'https://money.cnn.com/data/hotstocks/'
    page = requests.get(base_url)

    soup = BeautifulSoup(page.content, 'html.parser')

    container = soup.find(id = "wsod_hotStocks")

    headers = container.find_all('h3')
    final_dict = {}

    for header in headers:
        top10 = []
        table = header.find_next_sibling("table")
        all_rows = table.find_all("tr")
        del all_rows[0]
        for row in all_rows:
            a = row.find("a").text.strip()
            span = row.find("span").text.strip()
            stock_name = a + " " + span
            top10.append(stock_name)
        final_dict[header.contents[0]] = top10

    print("Which stock are you interested in: ")
    for key in final_dict:
        print(key + ":")
        for value in final_dict[key]:
            print(value)
        print("\n")

def stock_info():
    pass
# Part 1
hotstocks()
stock = input("User inputs: ")
# Part 2
stock_info()
pass
