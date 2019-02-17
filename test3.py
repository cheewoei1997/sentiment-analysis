import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

import nltk
from nltk.corpus import stopwords
from nltk.classify import SklearnClassifier
from nltk.classify import NaiveBayesClassifier

from wordcloud import WordCloud,STOPWORDS
import matplotlib.pyplot as plt

from subprocess import check_output
import os

# ==============================================================================

sentence = 'I feel great'

pos_words = open(os.path.join('datasets', 'positive-words.txt'), 'r').read()
neg_words = open(os.path.join('datasets', 'negative-words.txt'), 'r').read()
# print(neu_words)

pos_words = nltk.word_tokenize(pos_words)
neg_words = nltk.word_tokenize(neg_words)

def word_feats(words):
    return dict([(word, True) for word in words])

positive_features = [(word_feats(pos), 'pos') for pos in pos_words]
negative_features = [(word_feats(neg), 'neg') for neg in neg_words]

train_set = positive_features + negative_features
print(len(train_set))
print(positive_features)

classifier = NaiveBayesClassifier.train(train_set)

neg = 0
pos = 0
# sentence = "I feel terrible today."
sentence = sentence.lower()
print(sentence)
words = nltk.word_tokenize(sentence)

print(words)
for word in words:
    classResult = classifier.classify(word_feats(word))
    print(word_feats(word))
    print(classResult)
    if classResult == 'neg':
        neg = neg + 1
    if classResult == 'pos':
        pos = pos + 1
 
print('Positive: ' + str(float(pos)/len(words)))
print('Negative: ' + str(float(neg)/len(words)))
print('Pos', pos)
print('Neg', neg)

# print(positive_features)
# print(negative_features)

# print(pos_words)
# print(neg_words)