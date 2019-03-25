# coding: utf-8
import time
import random
import re
import json
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
mon0={
    '代表曲に「涙のキッス」「いとしのエリー」などがある桑田佳祐がリーダーの日本のロックバンドといえばなんでしょう？':'サザンオールスターズ',
    '中央ヨーロッパに位置するドイツ語圏の国で、首都がウィーンの国といえばどこでしょう？':'オーストリア',
    '1964年10月1日に開業した日本の高速鉄道で、「東海道」「山陽」「北陸」などの種類がある列車といえばなんでしょう？':'新幹線',
    'タイ語で、煮る、混ぜる、エビという意味がある、辛味と酸味、複雑な香りが特徴的なタイのスープ料理といえば何でしょう':'トムヤンクン',
    '円を描いたり、線分の長さを移すのに用いる物で、「ぶんまわし」や「両脚器（りょうきゃくき）」ともいう日本では小学校三年生で扱い始める文房具は何でしょう？':'コンパス'

}
mon1={'物体にはたらく力の合力が0ならば、運動している物体は等速直線運動を続け、静止している物体は静止し続ける。これを何と言う？':'慣性の法則'}
mon2={'同じ元素からなるが、結晶構造の違いなどによって性質の異なる単体どうしの事を漢字三文字で何と言う？':'同素体'}
ans = '答え'
@respond_to('quiz0')
def quiz0_func(message):
    global risten
    global ans
    if risten == 1:
        return
    message.send('問題です')
    monban = random.choice(list(mon0.keys()))
    time.sleep(1)
    message.send(mon0[monban])
    risten = 1
    ans = mon0[monban]
        
@respond_to('quiz1')
def quiz1_func(message):
    global risten
    global ans
    if risten == 1:
        return
    message.send('問題です')
    monban = random.choice(list(mon1.keys()))
    time.sleep(1)
    message.send(mon1[monban])
    risten = 1
    ans = mon1[monban]
        
@respond_to('help')
def help_func(message):
    message.send('botメンション時、quiz◯と入力すると問題が出題されます。')
    message.send('quiz0:クイズ quiz1:物理 quiz2:化学 quiz3:生物 quiz4:日本史 quiz5:世界史 quiz6:地理')
    message.send('回答するときは、「a」を入力し、回答権を得たら「a:答え」のように入力します。')
    message.send('問題を飛ばしたいときは、メンションしながら「pass」と打ちます。')

@respond_to('pass')
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
    message.reply('答えの前に a: を付けてチャットで回答してください。')
    ansuser = message.body['user']
    answait = 1

@listen_to(r'^a:')
def kaito_func(message):
    global anuser
    if answait == 0:
        return
    anuser = message.body['user']
    if anuser != ansuser:
        return
    text = message.body['text']
    textet = text.replace('a:', '')
    if textet == ans:
        message.reply('正解です')
    elif textet != ans:
        message.reply('残念。正解は ' + ans)
