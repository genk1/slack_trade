import re, json
import hmac
import hashlib
import requests
from future.moves.urllib.parse import urlencode
from slackbot.bot import respond_to
from slackbot.bot import listen_to

API_URL = "https://api.zaif.jp/api/1/"
secret = '<YOUR SECRET KEY HERE>'
key = '<YOUR API KEY HERE>'
g_nonce = 148

SUPPORTED_COIN = ["zaif","sjcx","btc","ncxc","cicc","xcp","xem","pepecash","jpyz","bitcrystals","bch","eth","fscc","mona", 'jpy']
MAIN_SUPPORTED_COIN = ["btc","xem","bch","eth","mona","zaif","pepecash"]

def get_deal_func(method, currency_pair, action, price, amount):
    global g_nonce
    params = {
        'nonce' : g_nonce,
        'method' : method,
        'currency_pair': currency_pair,
        'action': action,
        'price': price,
        'amount': amount
    }
    encoded_params = urlencode(params)
    signature = hmac.new(bytearray(secret.encode('utf-8')), digestmod=hashlib.sha512)
    signature.update(encoded_params.encode('utf-8'))
    headers = {
        'key': key,
        'sign': signature.hexdigest()
    }
    response = requests.post('https://api.zaif.jp/tapi', data=encoded_params, headers=headers)
    if response.status_code != 200:
        raise Exception('return status code is {}'.format(response.status_code))
    g_nonce += 1
    print(json.loads(response.text))
    return response

@respond_to(r'^trade\s+\S.*')
def trade_coin_func(message):
    slack_message = ""
    text = message.body['text'].lower()
    method, currency, action, price, amount = text.split(" ")
    currency_pair = currency + "_jpy"
    data = get_deal_func(method, currency_pair, action, price, amount).json()
    if data['success']:
        slack_message = "取引成功\n"
        slack_message = "取引後残高 : " + str(data['return']['funds']['jpy']) + "円"
        # funds = data['return']['funds']
        # for fund in funds:
        #     if fund.lower() in SUPPORTED_COIN:
        #         slack_message += fund + " : " + str(funds[fund])) + "\n"
    else:
        slack_message = "取引失敗\n"
        slack_message = data['error']
    message.reply(slack_message)
