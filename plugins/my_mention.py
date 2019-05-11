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
yen = "2000"
gas = {
    "チーズONチーズINハンバーグ":799,
    "チーズINハンバーグ":599,
    "チーズINハンバーグ＆エビフライ":849,
    "アボカドチーズINハンバーグ":849,
    "ハンバーグ＆エビフライ":699,
    "ハンバーグ＆チキン南蛮":799,
    "てりたまハンバーグ":549,
    "ミックスグリル":799,
    "ハンバーグステーキ":499,
    "肉盛り！ワイルドプレート":999,
    "チキチキ！ピリ辛スパイス焼き！":699,
    "若鶏のグリル　大葉おろしの醤油ソース":699,
    "若鶏のグリル　ガーリックソース":699,
    "若鶏の熟成醤油もろみ焼き":599,
    "ビーフカットステーキ":999,
    "ビーフカットステーキてんこもり":1299,
    "若鶏と彩り野菜の黒酢あん":499,
    "さばの味噌煮":399,
    "豚肉の生姜焼き":599,
    "焼き野菜と大葉おろしの和風ハンバーグ":599,
    "ミックスフライ":699,
    "若鶏の竜田揚げ　おろしポン酢":699,
    "豚ロースのおろしとんかつ":599,
    "マルゲリータピザ":599,
    "シュリンプベーコンピザ":799,
    "たっぷりマヨコーンピザ":499,
    "なすとほうれん草のミートソーシスパゲティ":699,
    "豆乳カルボナーラスパゲティ":699,
    "海老のトマトソーススパゲティ＆根菜とカリカリチーズの20品目シーザーサラダSサイズセット":878,
    "海老のトマトソーススパゲティ":599,
    "トマトソーススパゲティ　モッツアレラチーズトッピング":649,
    "トマトソーススパゲティ":499,
    "ピリ辛肉味噌担担麺＆ご飯セット":858,
    "ピリ辛肉味噌担々麺":699,
    "ピリ辛肉味噌担々麺（糖質控えめ・ほうれん草麺）":799,
    "1日分の野菜のベジ塩タンメン＆具だくさんフルーツヨーグルトセット":878,
    "1日分の野菜のベジ塩タンメン":699,
    "1日分の野菜のベジ塩タンメン（糖質控えめ・ほうれん草麺）":799,
    "特製本格辛口チゲ（半玉うどん入り）＆十三穀米セット":878,
    "特製本格辛口チゲ（半玉うどん入り）":699,
    "海老と山芋オクラのねばとろサラダうどん＆ほうれん草ベーコンセット":878,
    "海老と山芋オクラのねばとろサラダうどん":699,
    "糖質控えめ・海老と山芋オクラのねばとろサラダ麺（糖質控えめ・ほうれん草麺）":799,
    "オムライスビーフシチューソース＆ほうれん草ベーコンセット":878,
    "オムライスビーフシチューソース":699,
    "濃厚デミとさっぱりトマトのオムライス":799,
    "温玉ミートドリア":499,
    "ミートドリア":399,
    "ネギトロ丼":899,
    "ミニねぎとろ丼":449,
    "ひれかつ丼（味噌汁・漬物付き）":699,
    "海老ときのこの雑炊＆ちりめんじゃこと豆腐のねばとろサラダSサイズセット":928,
    "海老とキノコの雑炊":599,
    "おつまみコロッケ":199,
    "揚げたてアジフライ":199,
    "ちょい盛りポテトフライ":199,
    "コーンのオーブン焼き":199,
    "スナップエンドウとベーコンのオーブン焼き":199,
    "ソーセージグリル":199,
    "ほうれん草ベーコン":199,
    "若鶏の唐揚げ（５コ）":299,
    "山盛りポテトフライ":299,
    "豚肉てんこもやし":299,
    "海老とアボカドのタルタル仕立て":299,
    "トマトとモッツァレラのカプレーゼ風":299,
    "チキンとモッツァレラのトマトオーブン焼き":299,
    "ミニ牛タンシチュー":399,
    "トウモロコシのポタージュ":199,
    "ソフトフランスパン":179,
    "グリーンスムージー":299,
    "セットドリンクバー":219,
    "ストロベリーソースのベリーベリーパンケーキ":599,
    "チョコバナナとマスカルポーネのパンケーキ":599,
    "パリッと食感のチョコレートパフェ":499,
    "チョコバナナサンデー":399,
    "フォンダンショコラ　ソフトクリームトッピング":399,
    "フォンダンショコラ":299,
    "ソフトクリームあんみつ":399,
    "お濃い抹茶ババロア白玉あずきの盛り合わせ":399,
    "お濃い抹茶ババロア":199,
    "ぷるぷる黒糖ゼリー":199,
    "ぷるぷる黒糖ゼリー":299,
    "ソフトクリーム":279,
    "ソフトクリーム（ストロベリーソース）":299,
    "ソフトクリーム（黒糖きなこ）":299,
    "ベイクドチーズケーキ":299,
    "具沢山フルーツヨーグルト":199,
    "ライス":179,
    "十三穀米":229,
    "味噌汁":159,
    "日替わりスープ":159,
    "納豆":79,
    "とろろ":100,
}
@listen_to('ガスト1000')
def gast0_func(message):
    now = 0
    message.send('今日のガストガチャ(1000円コース)')
    while now < 927:
        if now > 725:
            zeikomi = int(now * 1.08)
            message.send(">合計 ¥"+ str(zeikomi) + " (税抜 ¥"+ str(now) + " )")
            break
        tabe = random.choice(list(gas.keys()))
        price = int(gas[tabe])
        if now + price < 927:
            now += price
            onezei = int(price*1.08)

            message.send(tabe + " ¥" + str(onezei))

@listen_to('ガスト1500')
def gast1_func(message):
    now = 0
    message.send('今日のガストガチャ(1500円コース)')
    while now < 1390:
        if now > 1188:
            zeikomi = int(now * 1.08)
            message.send(">合計 ¥"+ str(zeikomi) + " (税抜 ¥"+ str(now) + " )")
            break
        tabe = random.choice(list(gas.keys()))
        price = int(gas[tabe])
        if now + price < 1390:
            now += price
            onezei = int(price*1.08)

            message.send(tabe + " ¥" + str(onezei))

@listen_to('quiz0')
def quiz0_func(message):
    message.send("本業はちょっとお休みします。")
    return
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
        
@listen_to('!help')
def help_func(message):
    message.send('ガスト1000 または　ガスト1500 でガストのメニューを作ります。')
    message.send('quiz0:クイズ quiz1:物理 quiz2:化学 quiz3:生物 quiz4:日本史 quiz5:世界史 quiz6:地理')
    message.send('回答するときは、「a」を入力し、回答権を得たら「a:答え」のように入力します。')
    message.send('問題を飛ばしたいときは、「!pass」と打ちます。')

@listen_to('!pass')
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
@respond_to('ガスト1000')
def gastr_func(message):
    now = 0
    message.send('今日のガストガチャ(1000円コース)')
    while now < 927:
        if now > 725:
            zeikomi = int(now * 1.08)
            message.send(">合計 ¥"+ str(zeikomi) + " (税抜 ¥"+ str(now) + " )")
            break
        tabe = random.choice(list(gas.keys()))
        price = int(gas[tabe])
        if now + price < 927:
            now += price
            onezei = int(price*1.08)

            message.send(tabe + " ¥" + str(onezei))

@respond_to('ガスト1500')
def gastrr_func(message):
    now = 0
    message.send('今日のガストガチャ(1500円コース)')
    while now < 1390:
        if now > 1188:
            zeikomi = int(now * 1.08)
            message.send(">合計 ¥"+ str(zeikomi) + " (税抜 ¥"+ str(now) + " )")
            break
        tabe = random.choice(list(gas.keys()))
        price = int(gas[tabe])
        if now + price < 1390:
            now += price
            onezei = int(price*1.08)

            message.send(tabe + " ¥" + str(onezei))

