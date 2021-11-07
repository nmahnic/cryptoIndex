from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import CoinMarketCap
import sched, time
import datetime


url = CoinMarketCap.LISTINGS_LATEST
paramenters = {
    'start':'1',
    'limit': '15',
    'convert': 'USD'
}

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': CoinMarketCap.API_KEY
}

session = Session()
session.headers.update(headers)

s = sched.scheduler(time.time, time.sleep)

def doRequest(sc):
    print("-----------------------------------")
    print("REQUEST: ",datetime.datetime.now())
    try:
        response = session.get(url, params=paramenters)
        data = json.loads(response.text)
        # print(json.dumps(data, indent=4, sort_keys=True))
        datita = data["data"]
        # print(datita)
        cryptoDom = {}
        for crypto in datita:
            if("USD" in crypto['symbol'] or crypto['symbol'] == "DAI"):
                pass
            else:
                cryptoDom.update({crypto['symbol']:crypto["quote"]["USD"]["market_cap_dominance"]})
        # print(cryptoDom)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    sum = 0
    for dom in cryptoDom:
        sum += cryptoDom[dom]
    print(sum)

    for i, dom in enumerate(cryptoDom):
        if i >=10:
            break
        else:
            print(i+1,":",dom,"{:.4f}%".format((cryptoDom[dom]/sum)*100))
    s.enter(5*60,1, doRequest, (sc,))
    print("-----------------------------------")

s.enter(1,1, doRequest, (s,))
s.run()

"""si haces una request cada 5min, es decir 12 req por hora serian 8640 req al mes """