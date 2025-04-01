# Dash app: Stock index, currency pair and macroeconomic indicator
Example of plotly dash app. Store data into json structure via data_discovery_job.py executed via scheduler on main python file. given the way it is released on free tier VPS this is the simplest way to hanlde these kind of data with the few amount of resources avaialble. <br>

## Build and release docker image
To build the macro dashboard use the following command
’sudo docker build -t macro_app .’

To spin the container
’sudo docker run -it --rm -p 8050:8050 macro_app’