import requests

def fetch_rates():

    url = "https://api.nbp.pl/api/exchangerates/tables/A/?format=json"

    response = requests.get(url)

    return response.json()