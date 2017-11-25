# import re, requests, json
# import hmac
# import hashlib
# import requests
# from future.moves.urllib.parse import urlencode
# from zaifapi import ZaifPublicApi
# from slackbot.bot import respond_to
# from slackbot.bot import listen_to
#
# API_URL = "https://api.zaif.jp/api/1/"
# secret = '7302b9d5-79b7-4116-a89b-3885ab588e60'
# key = '4a7d7567-0874-4cb4-a6e2-838a9d5ebe8d'
#
# @respond_to(r'^trade\s+\S.*')
# def trade_coin_func(message):
#     secret = '7302b9d5-79b7-4116-a89b-3885ab588e60'
#     key = '4a7d7567-0874-4cb4-a6e2-838a9d5ebe8d'
#
#     params = {
#         'nonce' : 129,
#         'method' : 'trade',
#         'currency_pair': 'xem_jpy',
#         'action': 'ask',
#         'price': '22.52',
#         'amount': '0.1'
#     }
#     encoded_params = urlencode(params)
#     signature = hmac.new(bytearray(secret.encode('utf-8')), digestmod=hashlib.sha512)
#     signature.update(encoded_params.encode('utf-8'))
#     headers = {
#         'key': key,
#         'sign': signature.hexdigest()
#     }
#     response = requests.post('https://api.zaif.jp/tapi', data=encoded_params, headers=headers)
#     if response.status_code != 200:
#         raise Exception('return status code is {}'.format(response.status_code))
#     print(json.loads(response.text))
