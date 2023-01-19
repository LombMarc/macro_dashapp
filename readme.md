# Dash app: Stock index, currency pair and macroeconomic indicator
This is an example on how to build a dash app and deploy it using render. After building the app and launching it in your local host, is possible to access render.com and deploy on a free virtual machine the web app. To do so we need to specify the libraries required by the virtual machine. <br>
After connecting to github is possible to select the repository from which render will deploy the app. <br>
Here https://macro-dashapp.onrender.com you can see the app running, the loading time is a bit longer than normal since:
1. it is deployed on the free version and so it has lower specs than an avarage computer and we server,
2. the script will first scrape some website to retrive the new data and then will build the figure and define the layout of the page.
<br>
