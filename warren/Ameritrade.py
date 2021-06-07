import requests
import json


markets = ["EQUITY", "OPTION", "FUTURE", "BOND", "FOREX"]
# api-endpoint
URL = "https://api.tdameritrade.com/v1/marketdata/hours"

# defining a params dict for the parameters to be sent to the API
for market_type in markets:
    PARAMS = {'apikey': 'F5XKKXXRKYERXP2HHZ5HEOHXAQRIFL1E', 'markets': market_type, 'date': '2021-02-10'}

    # sending get request and saving the response as response object
    r = requests.get(url=URL, params=PARAMS)

    # extracting data in json format
    data = json.loads(r.text)
    f = open(market_type+"_response.json", "w")
    f.write(json.dumps(data, indent=4))
    f.close()

