# slack_trade
今年3月からzaifを使って暗号通貨取引を開始したのだが、bot取引をしてみたいと思い少しずつ進めていきたいと思います。

目標
 - ボットによる自動取引
 - アービトラージによる値格差取引

それでは今回行ったことですが、
「Slackを利用して簡単に購入、値段確認ができるようにしました」

### 必要なもの
1. python3系
2. pip install slackbot - [参考リンク>> https://github.com/lins05/slackbot](https://github.com/lins05/slackbot)
3. 購入まで行いたい人は API KEY 発行 [参考リンク>> https://zaif.jp/api_keys](https://zaif.jp/api_keys)
4. SlackAPIと利用するためのチーム (webのSlackに入ったら https://チーム名.slack.com/appsへログインしてbotを検索して利用する -> 詳細は現在省く)

### 前提条件
slackでボットに対して
price xem
price btc
price all
などと送ると現在の価格表が返ってくるようにする

### 達成後のイメージ
<img width="520" alt="Screen Shot 2017-11-26 at 12.36.49 AM.png" src="https://qiita-image-store.s3.amazonaws.com/0/94541/0585c67f-d471-998d-c6f2-c62f56fae731.png">


### 作業手順
1. 適当なプロジェクトフォルダの作成
2. 価格表を取れるようにする (今回はここまで)
3. 購入を出来るようにする

## 1 . 適当なプロジェクトフォルダの作成

ここで行っていくのはslackbot libを利用するにあたり必要なプロジェクト構成を説明します。
-- プロジェクトフォルダ
-- -- run.py (実際に走らせるアプリ - 特に変更なし)
-- -- slackbot_settings.py (Slackボットの設定ファイル)
-- -- plugins
-- -- -- price_bot.py(価格表を取るサービス)
-- -- -- trade_bot.py(取引を実際にするサービス)

```python:run.py
# run.py

from slackbot.bot import Bot
def main():
    bot = Bot()
    bot.run()

if __name__ == "__main__":
    print('slackbot start')
    main()
```

```slackbot_settings.py
#slackbot_settings.py

# slack bot API
API_TOKEN = "xoxb-<YOUR API TOKEN HERE>"

# ボットがキーワードを理解できなかった場合に返すデフォルトメッセージ
DEFAULT_REPLY = "ゴメン！理解ができなかったよ。(/ω・＼)ﾅｷｯ"

# pluginsフォルダへパスを通すことによってpluginsフォルダ内に入っている全てのサービスを運用することが出来るようになる
PLUGINS = ['plugins']
```
上記の設定をまず行ったら、pluginフォルダ内にまずはサービスファイルを作ってみよう!!

今回は現在の価格がわかるようにするためのサービスを作ってみる。

前提条件

```python:price_bot.py
#price_bot.py

import re, requests, json
from slackbot.bot import respond_to # Slackで送られてきたキーワードに対して返答を返すため
```
必要なグローバルvariableを設定

```python:price_bot.py
# 今回利用する現物公開APIの元URL
API_URL = "https://api.zaif.jp/api/1/"
# サポートされている通貨リスト 全て日本円(fiat)との価格差を想定
SUPPORTED_COIN = ["zaif","sjcx","btc","ncxc","cicc","xcp","xem","pepecash","jpyz","bitcrystals","bch","eth","fscc","mona"]
# 私事ではあるが、メインで取引している通貨
MAIN_SUPPORTED_COIN = ["xem","zaif","btc","bch","mona","pepecash","eth"]
```

```python:price_bot.py
@respond_to(r'^price\s+\S.*')
def price_coin_func(message):
    slack_message = ""
    text = message.body['text'].lower() # 大文字を全て小文字に
    # 前提条件として送られてくるキーワードは２つ
    # price coin名
    method, coin_name = text.split(" ") 
    if coin_name == 'all':
        # 最初に決めている私のメイン通貨のみの確認この場合は現在の価格のみを取得する
        for main_coin in MAIN_SUPPORTED_COIN:
            data = get_last_price_func(main_coin + "_jpy").json()
            slack_message += main_coin + " - 現在の価格 : " + str(data['last_price']) + "\n"
    elif coin_name not in SUPPORTED_COIN:
        # サポート外の通貨に対するエラーメッセージ メッセージを直打ちにしたのはあまり意味はない
        slack_message = "対象の通貨 : " + coin_name + " は、サポートされていません。\n サポート対象通貨は：\n"
        slack_message += "\n".join(SUPPORTED_COIN)
    else:
        # 指定通貨の過去24時間の値動きなども併せて表示
        data = get_trade_detail_func(coin_name + "_jpy").json()
        slack_message = coin_name + 'の価格 : \n 買気配 : ' + str(data['bid']) + '\n 売気配 : ' + str(data['ask']) + '\n最高額 : ' + str(data['high']) + '\n最低額 : ' + str(data['low'])
    message.reply(slack_message)
```


```python:price_bot.py
# 指定通貨が存在した場合の詳細ticker情報を取る場合
def get_trade_detail_func(coin_type):
    request_data = requests.get(
        API_URL + 'ticker/' + coin_type
        , headers = {
        })
    return request_data
```


```python:price_bot.py
# 全てのメイン通貨現在価格を取得したい場合
def get_last_price_func(coin_type):
    request_data = requests.get(
        API_URL + 'last_price/' + coin_type
        , headers = {
        })
    return request_data
```

ここまでやってみて、「あっ、これなら一つにまとめられるやん！」
ということに気づく。。。

ちょっと戻って、

```python:price_bot.py
#data = get_last_price_func(main_coin + "_jpy").json()
data = get_price_func(main_coin + "_jpy", 'last_price/').json()
*


#data = get_trade_detail_func(coin_name + "_jpy").json()
data = get_price_func(coin_name + "_jpy", 'ticker/').json()

# 一つにまとめてあげる
def get_price_func(currency_pair, action):
    request_data = requests.get(
        API_URL + action + currency_pair
        , headers = {
        })
    return request_data

```
と変更！
こっちのほうがスッキリしましたね！
というかこれであれば基本的に現金取引のAPIを叩きたいときは直ぐに呼び出せるようになりましたね！

### 以上で終了！

##ボリュームがでかくなってきたので今日はこれまでです！
次回は実際に取引をどのように行うかを書いていきたいと思います。

Zaifに興味がある方はこちらからどうぞ！(アフィですが！)
[Zaifへのリンク](https://zaif.jp?ac=6d3fmuu1ar)
            

### 今後の予定
0. -今回- Slackを利用して簡単に価格表を取得できるようにする
1. (次回) Slackを利用して簡単に購入ができるようにする
2. python 非公式APIに切り替える
3. AWSに設置していつでも使えるようにする(苦手)
4. websocketによるstreamによるデータ取得を行う
5. アビトラが出来るように他の取引所間での価格差を取得計算させ取引ができるようにする
6. ボットによる自動取引(FXの取引手法参照)

