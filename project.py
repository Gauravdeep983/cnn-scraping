from bs4 import BeautifulSoup
import requests
import csv

final_dict = {}
# ticker_list = {}

# Hotstocks page
def hotstocks():
    base_url = 'https://money.cnn.com/data/hotstocks/'
    page = requests.get(base_url)

    soup = BeautifulSoup(page.content, 'html.parser')

    container = soup.find(id="wsod_hotStocks")

    headers = container.find_all('h3')

    print("Which stock are you interested in: ")
    for header in headers:
        ticker_list = {}
        table = header.find_next_sibling("table")
        all_rows = table.find_all("tr")
        # Remove the header row
        del all_rows[0]
        for row in all_rows:
            a = row.find("a").text.strip()
            span = row.find("span").text.strip()
            # stock_name = a + " " + span
            ticker_list[a] = span
        final_dict[header.contents[0]] = ticker_list

    for category in final_dict:
        print(category + ":")
        for k,v in final_dict[category].items():
            print(k+" "+v)
        print("\n")


def stock_info(ticker):
    url = "https://money.cnn.com/quote/quote.html?symb=" + ticker
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')
    name = soup.find("h1", class_="wsod_fLeft").text.strip()
    header = soup.find("h3", class_="wsod_moduleTitle", text="Today’s Trading")
    container = header.find_next_sibling("div")
    table = container.find("table")
    stock_details = dict()
    for row in table:
        # for item in row:
        title = row.find("td").text.strip()
        value = row.find("td", class_="wsod_quoteDataPoint").text.strip()
        stock_details[title] = value
    # Formatting the dict and removing unnecessary details
    del stock_details["Day’s range"]
    del stock_details["Average volume (3 months)"]
    stock_details["Ticker"] = ticker
    stock_details["Name"] = name
    return stock_details


def export_csv():
    # Get details
    exporting_list = []
    for category in final_dict:
        for ticker,title in final_dict[category].items():
            # Format data for CSV
            temp_list = []
            temp_list.append(category)
            stock = stock_info(ticker)
            temp_list.append(ticker)
            temp_list.append(title)
            temp_list.append(stock["Today’s open"])
            temp_list.append(stock["Previous close"])
            temp_list.append(stock["Volume"])
            temp_list.append(stock["Market cap"])
            exporting_list.append(temp_list)
    # Export
    with open('stocks.csv', mode='w') as csv_file:
        writer =  csv.writer(csv_file)
        writer.writerows(exporting_list)

# Part 1
hotstocks()
ticker = input("User inputs: ")
ticker = "COTY"
# Part 2
stock_details = stock_info(ticker)
print("The data for "+ticker+" "+stock_details["Name"]+" is the following: ")
print("OPEN: "+stock_details["Today’s open"])
print("PREV CLOSE: "+stock_details["Previous close"])
print("VOLUME: "+stock_details["Volume"])
print("MARKET CAP: "+stock_details["Market cap"])
# Part 3
export_csv()
