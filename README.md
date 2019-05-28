# Asked-Aimyon

##  あいみょんに「愛」とは何か聞いてみた


## 使用技術

* Python 3.7.3 
* 自然言語処理(mecab, word2vec)
* スクレイピング(BeautifulSoup)



## 使用方法

### クローン

```
git clone https://github.com/k4ssyi/Asked-Aimyon.git
```

### 仮想環境準備
```
$ python -m venv .venv
$ source .venv/bin/activate
```

### pipfileからライブラリをインストール

```
$ pip install pipenv
$ pipenv install 
```

### 歌詞ページをスクレイピングする
```
$ python scraping.py
```

lyrics.txt に歌詞が保存される

### 歌詞を解析する
```
$ python analysis.py
```
