import nltk


pos_list = ['good', 'great', 'best']
neg_list = ['bad', 'worse', 'worst']
sentence = 'I am bad good great bestest best'

posneg = pos_list + neg_list
print(posneg)

sentence = nltk.word_tokenize(sentence)

neu_list = []
[neu_list.append(neu) for neu in sentence if neu not in posneg]
print(neu_list)
# [x for x in item if x not in z]
# print(x)