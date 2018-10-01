import json, random
from gensim.models.word2vec import Word2Vec
from gensim.models import KeyedVectors
import numpy as np
from sklearn.externals import joblib
from operator import itemgetter

# load data
json1 = open('markov_gingatetsudono_yoru_ow.json', 'r')
rawdata = json.load(json1)
model = Word2Vec.load('wikimodel/word2vec.gensim.model')

# words to start
_1 = '野球'
_2 = 'する'
print('')

flag1 = True # don't exist?
for row in rawdata:
	if row == _1:
		print('Beginning of sentence:',_1,'exists in the dictionary!')
		flag1 = False
		break
if flag1:
	print('Beginning of sentence:',_1,"doesn't exist in the dictionary!")
flag2 = True
for row in rawdata:
	if row == _2:
		print('End of sentence:',_2,'exists in the dictionary!')
		flag2 = False
		break
if flag2:
	print('End of sentence:',_2,"doesn't exist in the dictionary!")

print('Most similar to', _1 + ':')
print(model.most_similar(_1,[],5))
print('Most similar to', _2 + ':')
print(model.most_similar(_2,[],5))
print('')

period = model.wv['。']
bos = model.wv[_1]
eos = model.wv[_2]
est13_2 = joblib.load('13_2.pkl')
est12_3 = joblib.load('12_3.pkl')
est23_1 = joblib.load('23_1.pkl')

#'''
# 3 words, 13_2 only
print('3 words, 13_2 only')
num_of_sentence = 9
_input = np.hstack((bos,eos))
inputs = [_input]
betweenVec = est13_2.predict(inputs)
words = model.most_similar(betweenVec,[],num_of_sentence)
sorted(words, key=lambda words: words[1])
for i in words:
	print(_1,i[0],_2,i[1])
print('')


# 4 words, 12_3 and 13_2 
print('4 words, 12_3 and 13_2 ')
num_of_words = 3
sentence = []
_2nd = est12_3.predict([np.hstack((period,bos))])
words = model.most_similar(_2nd,[],num_of_words)
for i in words:
	_3rd = est13_2.predict([np.hstack((model.wv[i[0]],eos))])
	words2 = model.most_similar(_3rd,[],num_of_words)
	for j in words2:
		sentence.append( [ _1, i[0], j[0], _2, j[1] ] )
sentence = sorted(sentence, key=itemgetter(4), reverse=True)
for line in sentence:
	mapped_list = map(str,line)
	printer = ' '.join(mapped_list)
	print(printer)
print('')


# 4 words, 23_1 and 13_2 
print('4 words, 13_2 and 23_1 ')
num_of_words = 3
sentence = []
_3rd = est23_1.predict([np.hstack((eos,period))])
words2 = model.most_similar(_3rd,[],num_of_words)
for i in words2:
	_2nd = est13_2.predict([np.hstack((bos,model.wv[i[0]]))])
	words = model.most_similar(_2nd,[],num_of_words)
	for j in words:
		sentence.append( [ _1, j[0], i[0], _2, j[1] ] )
sentence = sorted(sentence, key=itemgetter(4), reverse=True)
for line in sentence:
	mapped_list = map(str,line)
	printer = ' '.join(mapped_list)
	print(printer)
print('')
#'''

# Filling holes of famous sentences
famous_sentences = [
					[('吾輩',1),('猫',1),('ある','。')],
					[('国境',1),('長い',1),('を',1),('と',1),('で',1),('た','。')],
					[('天',1),('人',1),('上',1),('人',1),('作ら',1),('、',0),('人',1),('下',1),('人',1),('作ら',1),('。',0)]
]
num_of_words = 5

for sentence in famous_sentences:
	filled_sentence = []
	block_before = ('。',0)
	for index, block in enumerate(sentence):
		if index == 0:
			block_before = block
			filled_sentence.append(block[0])
			continue
		elif block[1] == '。' or block[0] == '。':
			between_vec = est13_2.predict([np.hstack((model.wv[block_before[0]],model.wv[block[0]]))])
			between_words = model.most_similar(between_vec, [], num_of_words)
			between_word = random.choice(list(between_words))
			filled_sentence.append(between_word[0])
			filled_sentence.append(block[0])
			if block[1] == '。':
				filled_sentence.append(block[1])
		elif block[1] == 1 or block[1] == 0:
			between_vec = est13_2.predict([np.hstack((model.wv[block_before[0]],model.wv[block[0]]))])
			between_words = model.most_similar(between_vec, [], num_of_words)
			between_word = random.choice(list(between_words))
			if between_word[0] == '、':
				between_word = random.choice(list(between_words))
			try:
				to_vec = model.wv[between_word[0]]
			except KeyError:
				between_word = random.choice(list(between_words))
			if block_before[1] != 0:
				filled_sentence.append(between_word[0])
				filled_sentence.append(block[0])
			else:
				filled_sentence.append(block[0])
			block_before = block
		else:
			words_to_fill = [('12_3',0) for i in range(block_before[1])]
			word_13_2 = words_to_fill[random.randint(range(block[1]))]
	printer = ' '.join(filled_sentence)
	print(printer)

'''
# make random sentence
print('Random sentences!')
num_of_words = 5
for i in range(3):
	top = rawdata["。"]
	keys = top.keys()
	first_word = "。"
	second_word = random.choice(list(keys))
	try:
		 to_vec = model.wv[second_word]
	except KeyError:
		second_word = random.choice(list(keys))
	last = ''
	sentence = [second_word]
	while (last != '。'):
		last_vec = est12_3.predict([np.hstack((model.wv[first_word],model.wv[second_word]))])
		lasts = model.most_similar(last_vec,[],num_of_words)
		last_word = random.choice(list(lasts))
		try:
			to_vec = model.wv[last_word[0]]
		except KeyError:
			last_word = random.choice(list(lasts))
		last = last_word[0]
		sentence.append(last)
		first_word = second_word
		second_word = last
	printer = ''.join(sentence)
	print(printer)
	print('----------------------')
'''
