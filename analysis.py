'''
MeCab.Tagger ("-Ochasen")の -Ochasenの部分はMeCabの出力モードです。

mecabrc:(引数なし)
-Ochasen: (ChaSen 互換形式)
-Owakati: (分かち書きのみを出力)
-Oyomi: (読みのみを出力)

'''

import MeCab
from gensim.models import word2vec
import re
import requests
from bs4 import BeautifulSoup

with open("lyrics.txt", encoding='utf-8') as f:
    lyrics = f.read()

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


def tagger(text):
    # 全部入りモード
    mecab = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
    # mecab = MeCab.Tagger("-Ochasen")
    mecab.parse('')  # 文字列がGCされるのを防ぐ
    node = mecab.parseToNode(lyrics)
    word_array = []
    stop_word = create_stop_word()

    while node:
        # 品詞を取得
        pos = node.feature.split(",")[0]
        # word_array.append(node.surface)
        # word_array.append(node.feature.split(",")[6])
        if pos == "名詞":
            if node.surface not in stop_word:
                word_array.append(node.surface)
        if pos == "動詞":
            if not node.feature.split(",")[6] in stop_word:
                word_array.append(node.feature.split(",")[6])
        if pos == "形容詞":
            if not node.feature.split(",")[6] in stop_word:
                word_array.append(node.feature.split(",")[6])
        if pos == "形容動詞":
            if not node.feature.split(",")[6] in stop_word:
                word_array.append(node.feature.split(",")[6])

        print('{0} , {1}'.format(node.surface, node.feature.split(",")))
        # 次の単語に進める
        node = node.next

    return word_array


sentence = [tagger(lyrics)]
model = word2vec.Word2Vec(sentence, size=200, min_count=4, window=4, iter=50)
print(model.wv.most_similar(positive=[u"愛"], topn=10))
