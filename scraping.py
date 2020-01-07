#!/usr/bin/env python
# -*- coding: utf-8 -*
import requests
from bs4 import BeautifulSoup
import re
import codecs


filename = "alice.txt"

h1StartMkup = "[size=30][b][i][color=#dd2fc0]"
h1EndMkup = "[/color][/b][/i][/size]"
h2StartMkup = "[size=25][b][i][color=#c0dd2f]"
h2EndMkup = "[/color][/b][/i][/size]"
preStartMkup = "[i]"
preEndMkup = "[/i]"


target_url = 'https://www.gutenberg.org/files/11/11-h/11-h.htm' # 不思議な国のアリス
#target_url = 'https://www.gutenberg.org/files/1513/1513-h/1513-h.htm' # ロミオとジュリエット
#target_url = 'https://www.gutenberg.org/files/1661/1661-h/1661-h.htm' # シャーロックホームズ


result = requests.get(target_url)
result.raise_for_status() # 例外処理



soup = BeautifulSoup(result.text, "html.parser")

# マークアップを設定
for tag in soup.find_all("h1"):
    tag.insert(0, h1StartMkup)
    tag.append(h1EndMkup)


for tag in soup.find_all("h2"):
    tag.insert(0, h2StartMkup)
    tag.append(h2EndMkup)

for tag in soup.find_all("pre"):
    #tag.insert(0, preStartMkup)
    #tag.append(preEndMkup)
    tag.string = preStartMkup + tag.getText() + preEndMkup

# ファイル書き込み
textStartFlag = 0
with open(filename, "w", encoding="UTF-8") as f:
    for e in soup.find_all(["p", "h1", "h2", "pre", "td"]):
        if(textStartFlag == 1): # 本文タイトルをh1タグで検出、h1があるまで出力しない
            print(e.getText(), file=f)
        else:
            tmp = e.getText()
            if h1StartMkup in tmp:
                textStartFlag = 1
                print(tmp, file=f)

# 改行処理
with open(filename, encoding="UTF-8") as f:
    column = 0
    pagecolumn = 20

    text = f.readlines()
    while True:
        if column == len(text):
            break
        
        if h2StartMkup in text[column]:
            while column % pagecolumn != 0:
                text.insert(column, "\n")
                column += 1
        column += 1

# 改行したデータでファイルを上書き
with open(filename, "w", encoding="UTF-8") as f:
    f.writelines(text)