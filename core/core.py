import bs4 as bs
import requests
import pandas as pd
import yfinance as yf
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def Euribor():
    page = requests.get("https://www.euribor-rates.eu/it/")
    soup = bs.BeautifulSoup(page.text, 'lxml')
    table = soup.find('table')
    rates = pd.read_html(str(table))[0]
    rates['Maturity'] = [1 / 52, 1 / 12, 0.25, 0.5, 1]
    rates['Rate'] = [float(i[:-1].replace(",", ".")) / 100 for i in rates[rates.columns[1]].tolist()]
    # print(rates.drop([0,1],axis=1))
    return rates

def define_webdriver():
    options = Options()
    options.add_argument('--headless')  
    options.add_argument('--disable-gpu')  
    options.add_argument('--no-sandbox')  

    driver = webdriver.Chrome(options=options)

    return driver

def yield_rate(country:str,driver):
    page = f"http://www.worldgovernmentbonds.com/country/{country}/"
      
    driver.get(page)
    time.sleep(2)  
    soup = bs.BeautifulSoup(driver.page_source, 'lxml')
    
    with open('../page_html.html', 'w') as fl:
        fl.write(soup.prettify())
    
    table = soup.find('table', {'id': 'table-curve'})
    rows = []
    for row in table.find_all('tr'):
        try:
            cols = row.find_all(['th', 'td'])
            cols = [col.text.strip() for col in cols][1:3]
            cols = [cols[0],cols[1].replace("%","")]
            rows.append(cols)
        except:
            break
    rows = rows[2:]
    rates = pd.DataFrame(rows,columns=["Maturity","Yield"])
    rates["Yield"] = (rates["Yield"]).astype("float")/100
    #need to convert month/year to real number for line chart order
    time_mapping = {
        'month': 1 / 12,
        'months': 1 / 12,
        'year': 1,
        'years': 1
    }
    rates['Maturity'] = rates['Maturity'].apply(lambda x: float(x.split()[0]) * time_mapping[x.split()[1].lower()])

    return rates

def get_inflation(country:str):
    page = requests.get(f"https://www.rateinflation.com/inflation-rate/{country}/")
    soup = bs.BeautifulSoup(page.text, 'lxml')
    table = soup.find('table')
    rates = pd.read_html(str(table))[0]
    # print(rates)
    for i in rates.columns[1:-1]:
        rates[i] = rates[i].str.rstrip('%').astype(float) / 100
    return rates

def economic_calendar():
    page = requests.get("https://www.myfxbook.com/forex-economic-calendar")
    soup = bs.BeautifulSoup(page.text, 'lxml')
    table = soup.find_all(id="economicCalendarContent")
    df = pd.read_html(str(table))[0].iloc[1:-1]
    n_df = df[[df.columns[0]]].copy()
    n_df['Cur'] = df[df.columns[3]].copy()
    n_df['Event'] = df[df.columns[4]].copy()
    return n_df.iloc[:-1].head(25)

def GDP_g20():
    page = requests.get("https://statisticstimes.com/economy/projected-world-gdp-ranking.php")
    soup = bs.BeautifulSoup(page.text, 'lxml')
    table = soup.find_all('table')
    rates = pd.read_html(str(table))[1]
    rate = pd.DataFrame()
    rate['Country'] = rates[rates.columns[0]]
    rate[rates.columns[1][-1]] = rates[list(rates.columns)[1]]
    rate[rates.columns[3][-1]] = rates[list(rates.columns)[3]]
    rate['Growth (%)'] = ((rate[rates.columns[3][-1]] - rate[rates.columns[3][-1]])/rate[rates.columns[3][-1]])*100
    return rate



