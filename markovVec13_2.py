import json
from gensim.models.word2vec import Word2Vec
from gensim.models import KeyedVectors
import numpy as np
from sklearn.externals import joblib

# load data
json1 = open('markov_gingatetsudono_yoru_ow.json', 'r')
rawdata = json.load(json1)
model = Word2Vec.load('wikimodel/word2vec.gensim.model')

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
            out2 = model.wv[q]
            in3 = model.wv[r]
            _input = np.hstack((in1,in3))
            data.append(_input)
            label.append(out2)

print('err:',len(err))

from sklearn.multioutput import MultiOutputRegressor
from sklearn import svm
est = MultiOutputRegressor(svm.SVR())
est.fit(data, label)

# save the parameters
joblib.dump(est, '13_2.pkl', compress=True) 