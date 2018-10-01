import json
from gensim.models.word2vec import Word2Vec
from gensim.models import KeyedVectors
import numpy as np
from sklearn.externals import joblib

# load data
json1 = open('markov_gingatetsudono_yoru_ow.json', 'r')
rawdata = json.load(json1)
model = Word2Vec.load('wikimodel/word2vec.gensim.model')
#model = KeyedVectors.load_word2vec_format('entity_vector.model.bin', binary=True)

# change utf-8 data to vector and insert it into the data or the label
data = []
label = []

err = []
for row in rawdata:
    p = row
    try:
        pp = model.wv[p]
    except KeyError:
        err.append(row)
        continue
    for row2 in rawdata[row]:
        q = row2
        try:
            qq = model.wv[q]
        except KeyError:
            mess = row2+' from row: '+row
            err.append(mess)
            continue
        for row3 in rawdata[row][row2]:
            r = row3
            try:
                rr = model.wv[r]
            except KeyError:
                mess = row3+' from row2: '+row2+' from row: '+row
                err.append(mess)
                continue
            in1 = model.wv[p]
            in2 = model.wv[q]
            out3 = model.wv[r]
            _input = np.hstack((in1,in2))
            data.append(_input)
            label.append(out3)

print('err:',len(err))

# training
# separating data into train data sets and test data sets
#from sklearn.model_selection import train_test_split
#X_train,X_test,y_train,y_test=train_test_split(data,label,test_size=0.25,random_state=33)

from sklearn.multioutput import MultiOutputRegressor
from sklearn import svm
clf5 = MultiOutputRegressor(svm.SVR())
clf5.fit(data, label)

# prediction
#print('SVR',clf5.score(X_test,y_test))

# 予測モデルをシリアライズ
joblib.dump(clf5, '12_3.pkl', compress=True) 