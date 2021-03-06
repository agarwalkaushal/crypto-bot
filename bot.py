import hmac
import hashlib
import json
import time
import requests
import schedule
import time

key = "011312b4a5b3712d52fe84f2e0e80bdb13159ea8a3821a2b"
secret = "f3fcf2dc3ce4ef6897cb5acbb3bb7e4aa33810128d1044886ec030a23de5b99f"
secret_bytes = bytes(secret, encoding='utf-8')


def get_balance(ticker):
    timeStamp = int(round(time.time() * 1000))
    body = {
        "timestamp": timeStamp
    }
    json_body = json.dumps(body, separators=(',', ':'))
    signature = hmac.new(secret_bytes, json_body.encode(),
                         hashlib.sha256).hexdigest()
    url = "https://api.coindcx.com/exchange/v1/users/balances"
    headers = {
        'Content-Type': 'application/json',
        'X-AUTH-APIKEY': key,
        'X-AUTH-SIGNATURE': signature
    }
    response = requests.post(url, data=json_body, headers=headers)
    data = response.json()
    for i in data:
        if i['currency'] == ticker:
            return i


def get_live_price(ticker):
    url = "https://api.coindcx.com/exchange/ticker"
    response = requests.get(url)
    data = response.json()
    for i in data:
        if i['market'] == ticker:
            return i


# def check_prices():
#     print("BTC: ", get_live_price('BTCINR')['last_price'])
#     print("ETH: ", get_live_price('ETHINR')['last_price'])


def create_order(ticker, quantity, action, price):
    timeStamp = int(round(time.time() * 1000))
    body = {
        "side": action,
        # "order_type": "market_order",
        "order_type": "limit_order",
        "market": ticker,
        "price_per_unit": price,
        "total_quantity": quantity,
        "timestamp": timeStamp
    }
    json_body = json.dumps(body, separators=(',', ':'))
    signature = hmac.new(secret_bytes, json_body.encode(),
                         hashlib.sha256).hexdigest()
    url = "https://api.coindcx.com/exchange/v1/orders/create"
    headers = {
        'Content-Type': 'application/json',
        'X-AUTH-APIKEY': key,
        'X-AUTH-SIGNATURE': signature
    }
    response = requests.post(url, data=json_body, headers=headers)
    data = response.json()
    print(data)


def program():
    inr_balance = get_balance('INR')
    print('INR: ', inr_balance['balance'])
    # Ethereum
    eth_price = get_live_price('ETHINR')['last_price']
    print('ETH: ', eth_price)
    if float(inr_balance['balance']) > 150:
        if float(eth_price) <= 160000:
            create_order('ETHINR', round(
                150/float(eth_price), 4), 'buy', eth_price)
    # Bitcoin
    btc_price = get_live_price('BTCINR')['last_price']
    print('BTC: ', btc_price)
    if float(inr_balance['balance']) > 150:
        if float(btc_price) <= 2400000:
            create_order('BTCINR', round(
                150/float(btc_price), 4), 'buy', btc_price)

    # if float(eth_price) > 210000:
        # create_order('ETHINR', round(150/float(eth_price), 4), 'sell', 210001)


def doge():
    inr_balance = get_balance('INR')
    print('Wallet: ', inr_balance)
    doge_price = get_live_price('DOGEINR')['last_price']
    print('Doge: ', doge_price)
    if float(inr_balance['balance']) > 4000:
        if float(doge_price) <= 32.35:
            create_order('DOGEINR', 10, 'buy', doge_price)

    if float(doge_price) >= 32.85:
        create_order('DOGEINR', 10, 'sell', doge_price)


schedule.every(30).seconds.do(program)

while 1:
    schedule.run_pending()
    time.sleep(1)
