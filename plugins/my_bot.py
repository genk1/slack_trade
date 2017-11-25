# from slackbot.bot import respond_to
# from slackbot.bot import listen_to
# import re, requests, json
#
# ZF_API_URL = "https://api.zaif.jp/api/1/"
# CC_API_URL = "https://coincheck.com/"
# BF_API_URL = "https://api.bitflyer.jp/v1/"
# API_KEY = ""
#
# def get_price_api(path, market = 'zf'):
#     method = 'GET'
#     request_url = ""
#     if market == 'zf':
#         request_url = ZF_API_URL
#     elif market == 'cc':
#         request_url = CC_API_URL
#     elif market == 'bf':
#         request_url = BF_API_URL
#     request_data = requests.get(
#         request_url + path
#         , headers = {
#         })
#     return request_data
#
# @respond_to('btc', re.IGNORECASE)
# def mention_func(message):
#     float("{0:.2f}".format(x))
#     data = get_price_api('ticker/btc_jpy', 'zf').json()
#     message.reply('ZF-BTC - 取引量 : ' + str(data['volume']) + ' 最高額 : ' + str(data['bid']) + ' 最低額 : ' + str(data['ask']))
#     data = get_price_api('api/ticker', 'cc').json()
#     message.reply('CC-BTC - 取引量 : ' + str(float("{0:.2f}".format(data['volume']))) + ' 最高額 : ' + str(data['bid']) + ' 最低額 : ' + str(data['ask']))
#     data = get_price_api('getticker', 'bf').json()
#     message.reply('BF-BTC - 取引量 : ' + str(data['volume']) + ' 最高額 : ' + str(data['best_bid']) + ' 最低額 : ' + str(data['best_ask']))
#
# @respond_to('xem', re.IGNORECASE)
# def mention_func(message):
#     data = get_price_api('ticker/xem_jpy').json()
#     message.reply('ZF-XEM - 取引量 : ' + str(data['volume']) + ' 最高額 : ' + str(data['high']) + ' 最低額 : ' + str(data['low']))
#
# @respond_to('mona', re.IGNORECASE)
# def mention_func(message):
#     data = get_price_api('ticker/mona_jpy').json()
#     message.reply('ZF-MONA - 取引量 : ' + str(data['volume']) + ' 最高額 : ' + str(data['high']) + ' 最低額 : ' + str(data['low']))
