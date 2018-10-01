# -*- coding: utf-8 -*-

import MeCab
import sys
import os, re, json, random

#tagger = MeCab.Tagger('-F\s%f[6] -U\s%m -E\\n')
tagger = MeCab.Tagger('-Owakati')

#fi = open(sys.argv[1], 'r')
fo = open(sys.argv[2], 'w')

fi = open(sys.argv[1], 'rb').read()
text = fi.decode('utf-8')
text = re.split(r'\-{5,}',text)[2] # ヘッダを削除
text = re.split(r'底本：', text)[0] # フッタを削除
text = text.strip()
text = text.replace('｜', '') # ルビの開始記号を削除
text = re.sub(r'《.+?》', '', text) # ルビを削除
text = re.sub(r'［＃.+?］', '', text) # 入力注を削除

'''
line = fi.readline()
while line:
    result = tagger.parse(line)
    fo.write(result[1:]) # skip first \s
    line = fi.readline()
'''
for line in text.split("\n"):
	result = tagger.parse(line)
	fo.write(result) # skip first \s

fi.close()
fo.close()