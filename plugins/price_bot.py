import re, requests, json
from slackbot.bot import respond_to
from slackbot.bot import listen_to

API_URL = "https://api.zaif.jp/api/1/"

SUPPORTED_COIN = ["zaif","sjcx","btc","ncxc","cicc","xcp","xem","pepecash","jpyz","bitcrystals","bch","eth","fscc","mona"]
MAIN_SUPPORTED_COIN = ["btc","xem","bch","eth","mona","zaif","pepecash"]

def get_price_func(currency_pair, action):
    request_data = requests.get(
        API_URL + action + currency_pair
        , headers = {
        })
    return request_data

@respond_to(r'^price\s+\S.*')
def price_coin_func(message):
    slack_message = ""
    text = message.body['text'].lower()
    method, coin_name = text.split(" ")
    if coin_name == 'all':
        for main_coin in MAIN_SUPPORTED_COIN:
            data = get_last_price_func(main_coin + "_jpy", 'last_price/').json()
            slack_message += main_coin + " - 現在の価格 : " + str(data['last_price']) + "\n"
    elif coin_name not in SUPPORTED_COIN:
        slack_message = "対象の通貨 : " + coin_name + " は、サポートされていません。\n サポート対象通貨は：\n"
        slack_message += "\n".join(SUPPORTED_COIN)
    else:
        data = get_trade_detail_func(coin_name + "_jpy", 'ticker/').json()
        slack_message = coin_name + 'の価格 : \n 買気配 : ' + str(data['bid']) + '\n 売気配 : ' + str(data['ask']) + '\n最高額 : ' + str(data['high']) + '\n最低額 : ' + str(data['low'])
    message.reply(slack_message)
