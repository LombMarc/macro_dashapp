from core.core import Econ_Calendar, define_webdriver, Yield_rates, Inflation, Euribor ,GDP, time
import json
import os

def store_data_writer(json_dict, filename):
    path = os.getcwd()+"/data"
    try:
        os.mkdir(path)
    except FileExistsError:
        print("folder alredy crated")
    path = path+f"/{filename}"
    with open (path, 'w') as f:
        #f.write(json.dumps(json_dict))
        json.dump(json_dict, f, indent=2, ensure_ascii=False)
    f.close()

def store_daily_data(path='data/calendar.json'):
    print("handling daily data")
    calend = Econ_Calendar()
    calend.scrape_and_produce()
    store_data_writer(calend.convert_to_json(),'calendar.json')


def store_long_term_data():
    print("handling long term data")
    web_driver = define_webdriver()
    yield_rates =  Yield_rates()
    yield_data_collection = {}
    for country in ['germany','italy','united-kingdom','united-states']:
        yield_rates.scrape_and_produce(web_driver,country)
        yield_data_collection[country] = (yield_rates.convert_to_json())

    store_data_writer(yield_data_collection,'yield_curves.json')

    inflation_data_collection = {}
    inflation = Inflation()
    for country in ['italy-inflation-rate','euro-area-historical-inflation-rate', 'usa-inflation-rate']:
        inflation.scrape_and_produce(country)
        inflation_data_collection[country] = (inflation.convert_to_json())

    store_data_writer(inflation_data_collection,'inflation.json')

    euribor = Euribor()
    euribor.scrape_and_produce()
    store_data_writer(euribor.convert_to_json(),'euribor.json')

    gdp = GDP()
    gdp.scrape_and_produce()
    store_data_writer(gdp.convert_to_json(),'gdp.json')
    
    
if __name__ == '__main__':
    if time.ctime().split(" ")[2] == '1':
        
        store_long_term_data()
        store_daily_data()
    else:
        store_daily_data()

