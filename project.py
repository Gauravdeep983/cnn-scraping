from bs4 import BeautifulSoup
import requests
import csv

final_dict = {}

# Method returns the CNN Hotstocks page details
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
        # Removing the header row
        del all_rows[0]
        for row in all_rows:
            a = row.find("a").text.strip()
            span = row.find("span").text.strip()
            ticker_list[a] = span
        final_dict[header.contents[0]] = ticker_list

    for category in final_dict:
        print(category + ":")
        for k, v in final_dict[category].items():
            print(k+" "+v)
        print("\n")

# Method returns details of a specific stock
def stock_info(ticker):
    url = "https://money.cnn.com/quote/quote.html?symb=" + ticker
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    not_found = soup.find("h1").text.strip()
    if (not_found != 'Symbol not found'):
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
        return stock_details, True
    else:
        return {}, False

# Method to create a CSV file with stock details
def export_csv():
    print("\nExporting CSV file..... (Takes approx 2-3 minutes)")
    exporting_list = []
    # Get each stock details from each each category (Losers, Gainers, etc)
    for category in final_dict:
        for ticker, title in final_dict[category].items():
            # Format data for CSV
            temp_list = []
            temp_list.append(category)
            stock = stock_info(ticker)
            temp_list.append(ticker)
            temp_list.append(title)
            temp_list.append(stock[0]["Today’s open"])
            temp_list.append(stock[0]["Previous close"])
            temp_list.append(stock[0]["Volume"])
            temp_list.append(stock[0]["Market cap"])
            exporting_list.append(temp_list)
    # Export CSV file
    with open('stocks.csv', mode='w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(exporting_list)


# Print stocks from 'CNN Money’s Market Movers' website
hotstocks()
try:
    # Get user input
    ticker = str(input("User inputs: ")).upper()
    # Get stock details using ticker
    stock_details, status = stock_info(ticker)
    if status is False:
        # If stock page not found   
        print("Stock ticker not found! Please try again.\n")
    else:
        print("The data for "+ticker+" " +stock_details["Name"]+" is the following: ")
        print("OPEN: "+stock_details["Today’s open"])
        print("PREV CLOSE: "+stock_details["Previous close"])
        print("VOLUME: "+stock_details["Volume"])
        print("MARKET CAP: "+stock_details["Market cap"])
        
        export_csv()
        print("\nDone!")
except ValueError:
    print("Invalid input!")
