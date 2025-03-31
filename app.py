from core.view import create_app

app = create_app()
server = app.server

'''if __name__ == '__main__':    
    app.run_server(port=80)
'''

from dash import Dash
import threading
import schedule
import time
from data_discovery_job import store_long_term_data, store_daily_data

def run_scheduled_task():
    schedule.every().day.at("07:30").do(store_daily_data)
    schedule.every().wednesday.at("15:00").do(store_long_term_data)
    
    while True:
        schedule.run_pending()
        time.sleep(40)  

if __name__ == "__main__":
    store_long_term_data()
    store_daily_data()
    scheduler_thread = threading.Thread(target=run_scheduled_task)
    scheduler_thread.daemon = True
    scheduler_thread.start()
    
    app.run_server(port=8050, debug=True)
else:
    store_long_term_data()
    store_daily_data()
    scheduler_thread = threading.Thread(target=run_scheduled_task)
    scheduler_thread.daemon = True
    scheduler_thread.start()
