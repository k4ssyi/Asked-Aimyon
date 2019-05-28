# import matplotlib.pyplot as plt
# from wordcloud import WordCloud
import requests
from bs4 import BeautifulSoup
import re

base_url = "https://www.uta-net.com"
target_url = "https://www.uta-net.com/search/?Aselect=1&Keyword=%E3%81%82%E3%81%84%E3%81%BF%E3%82%87%E3%82%93&Bselect=3&x=0&y=0"
music_num = 49
r = requests.get(target_url)

soup = BeautifulSoup(r.text, "html.parser")
url_list = []
# 曲一覧から各曲のURLを取り出してリストに入れる
for i in range(music_num):
    href = soup.find_all("td", attrs={"class": "side td1"})[
        i].contents[0].get("href")
    url_list.append(href)

lyrics = ""
# 曲ごとにRequestを送り歌詞を抽出する
for i in range(music_num):
    target_url = base_url + url_list[i]
    r = requests.get(target_url)
    soup = BeautifulSoup(r.text, "html.parser")

    for string in soup.find_all("div", attrs={"id": "kashi_area"})[0].strings:
        lyrics += string

with open('lyrics.txt', mode='w', encoding='utf-8') as fw:
    fw.write(lyrics)

# データの前処理
# 英数字の削除
lyrics = re.sub("[a-xA-Z0-9_]", "", lyrics)
# 記号の削除
lyrics = re.sub("[!-/:-@[-`{-~]", "", lyrics)
# 空白・改行の削除
lyrics = re.sub(u'\n\n', '\n', lyrics)
lyrics = re.sub(u'\r', '', lyrics)


def create_stop_word():
    target_url = 'http://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txt'
    r = requests.get(target_url)
    soup = BeautifulSoup(r.text, "html.parser")
    stop_word = str(soup).split()
    # 自分で追加
    my_stop_word = ['いる', 'する', 'させる', 'の', '色', '真夏', '身体', '最初', '知る', 'られる']
    stop_word.extend(my_stop_word)
    return stop_word
