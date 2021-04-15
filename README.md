# idx-shareholders

###### Dev Env
- ubuntu 20.08
- Python 3 venv
- LAMPP

###### Run
- install mysql client dev package of your OS
- install packages that listed in requirements.txt
- python main.py

###### Endpoints
- http://localhost:5002 (index) - simple front end to show list of share holders sorted by share value
- http://localhost:5002/v1/scraping - scrape list of stock share holders list from idx.co.id
- http://localhost:5002/v1/shareholders - index page requests this endpoint to get the list

