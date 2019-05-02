# coding: utf-8
import time
import random
import re
import json
import codecs
import feedparser
from slackbot.bot import respond_to     # @botname: で反応するデコーダ
from slackbot.bot import listen_to      # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ

# @respond_to('string')     bot宛のメッセージ
#                           stringは正規表現が可能 「r'string'」
# @listen_to('string')      チャンネル内のbot宛以外の投稿
#                           @botname: では反応しないことに注意
#                           他の人へのメンションでは反応する
#                           正規表現可能
# @default_reply()          DEFAULT_REPLY と同じ働き
#                           正規表現を指定すると、他のデコーダにヒットせず、
#                           正規表現にマッチするときに反応
#                           ・・・なのだが、正規表現を指定するとエラーになる？

# message.reply('string')   @発言者名: string でメッセージを送信
# message.send('string')    string を送信
# message.react('icon_emoji')  発言者のメッセージにリアクション(スタンプ)する
#                               文字列中に':'はいらない
risten = 0
answait = 0
ans = '答え'
@listen_to('quiz0')
def quiz0_func(message):
    global risten
    global ans
    global dd
    if risten == 1:
        return
    message.send('問題です')
    f = open('plugins/quiz.json', 'r')
    dd = json.load(f)
    monban = random.choice(list(dd.keys()))
    time.sleep(1)
    message.send(monban)
    risten = 1
    ans = dd[monban]
    f.close()
        
@listen_to('help')
def help_func(message):
    message.send('quiz◯と入力すると問題が出題されます。')
    message.send('quiz0:クイズ quiz1:物理 quiz2:化学 quiz3:生物 quiz4:日本史 quiz5:世界史 quiz6:地理')
    message.send('回答するときは、「a」を入力し、回答権を得たら「a:答え」のように入力します。')
    message.send('問題を飛ばしたいときは、「pass」と打ちます。')

@listen_to('pass')
def pas_func(message):
    global risten
    message.send('問題をパスします。')
    risten = 0

@listen_to('a')
def answer_func(message):
    global answait
    global ansuser
    if risten == 0:
        return   
    if answait == 1:
        return
    message.reply('答えの前に qq を付けてチャットで回答してください。')
    ansuser = message.body['user']
    answait = 1

@listen_to(r'^qq')
def kaito_func(message):
    global anuser
    global answait
    global risten
    if answait == 0:
        return
    anuser = message.body['user']
    if anuser != ansuser:
        return
    text = message.body['text']
    textet = text.replace('qq', '')
    if textet == ans:
        message.reply('正解です')
    elif textet != ans:
        message.reply('残念。正解は ' + ans)
    answait = 0
    risten = 0

@respond_to('a')
def ranswer_func(message):
    global answait
    global ansuser
    if risten == 0:
        return   
    message.reply('答えの前に qq を付けてチャットで回答してください。')
    answait = 1

@respond_to(r'^qq')
def rkaito_func(message):
    global anuser
    global answait
    global risten
    if answait == 0:
        return
    anuser = message.body['user']
    text = message.body['text']
    textet = text.replace('qq', '')
    if textet == ans:
        message.reply('正解です')

    elif textet != ans:
        message.reply('残念。正解は ' + ans)
    answait = 0
    risten = 0       
        
@respond_to('help')
def rhelp_func(message):
    message.send('quiz◯と入力すると問題が出題されます。')
    message.send('quiz0:クイズ quiz1:物理 quiz2:化学 quiz3:生物 quiz4:日本史 quiz5:世界史 quiz6:地理')
    message.send('回答するときは、「a」を入力し、回答権を得たら「a:答え」のように入力します。')
    message.send('問題を飛ばしたいときは、「pass」と打ちます。')
    message.send('')

@respond_to('pass')
def rpas_func(message):
    if answait == 0:
        return
    global risten
    message.send('問題をパスします。')
    risten = 0
#ここまでquiz機能
#ここからおまけ
@respond_to('spnews')
def rspnews_func(message):
    global yahoo_news_dic

    RSS_URL = "https://news.yahoo.co.jp/pickup/sports/rss.xml"

    yahoo_news_dic = feedparser.parse(RSS_URL)

    message.send(yahoo_news_dic.feed.title)

    for entry in yahoo_news_dic.entries:
        title = entry.title
        link  = entry.link
        message.send(link)
        message.send(title)
        break
    userid = message.body['user']
    f = open('plugins/quiz00.json','r')
    df = json.load(f)
    f.close()

@respond_to('itnews')
def ritnews_func(message):
    global yahoo_news_dic

    RSS_URL = "https://news.yahoo.co.jp/pickup/computer/rss.xml"

    yahoo_news_dic = feedparser.parse(RSS_URL)

    message.send(yahoo_news_dic.feed.title)

    for entry in yahoo_news_dic.entries:
        title = entry.title
        link  = entry.link
        message.send(link)
        message.send(title)
        break
    userid = message.body['user']
    f = open('plugins/quiz00.json','r')
    df = json.load(f)
    f.close()

@respond_to('mainnews')
def rmainnews_func(message):
    global yahoo_news_dic

    RSS_URL = "https://news.yahoo.co.jp/pickup/rss.xml"

    yahoo_news_dic = feedparser.parse(RSS_URL)

    message.send(yahoo_news_dic.feed.title)

    for entry in yahoo_news_dic.entries:
        title = entry.title
        link  = entry.link
        message.send(link)
        message.send(title)
        break
    userid = message.body['user']
    f = open('plugins/quiz00.json','r')
    df = json.load(f)
    f.close()
