import nltk
from nltk.corpus import stopwords
# from nltk.classify import SklearnClassifier
from nltk.classify import NaiveBayesClassifier
from nltk.collocations import BigramCollocationFinder

import sklearn
from nltk.classify.scikitlearn import  SklearnClassifier
from sklearn.svm import SVC, LinearSVC,  NuSVC
from sklearn.naive_bayes import  MultinomialNB, BernoulliNB
from sklearn.linear_model import  LogisticRegression
from sklearn.metrics import  accuracy_score

import os

# ==============================================================================

def word_feats(words):
    return dict([(words, True)])

def score(classifier):
    classifier = SklearnClassifier(classifier)
    classifier.train(train_set)
    pred = classifier.classify_many(words)
    n = 0
    s = len(pred)
    for i in range(0, s):
        if pred[i] == tag[i]:
            n = n + 1
    return n / s

sentence = 'Not only he is not well performed, he has not managed to get some valuable contacts as well.'
# sentence = 'He is not a happy and great guy.'
target = nltk.word_tokenize(sentence)

# Loads the positive and negative words
pos_words = open(os.path.join('datasets', 'positive-words.txt'), 'r').read()
neg_words = open(os.path.join('datasets', 'negative-words.txt'), 'r').read()
# print(neu_words)

# Tokenize the words
pos_words = nltk.word_tokenize(pos_words)
neg_words = nltk.word_tokenize(neg_words)

# Keep both positive and negative into posneg
posneg = pos_words + neg_words

neu_words = []
[neu_words.append(neu) for neu in target if neu not in posneg]
# print(pos_words)

positive_features = [(word_feats(pos), 'pos') for pos in pos_words]
negative_features = [(word_feats(neg), 'neg') for neg in neg_words]
neutral_features = [(word_feats(neu.lower()), 'neu') for neu in neu_words]

print(neutral_features)

train_set = positive_features + negative_features + neutral_features
print(len(train_set))
# print(positive_features)

# negcutoff = int(len(negative_features)*3/4)
# poscutoff = int(len(positive_features)*3/4)
 
# train_set = negative_features[:negcutoff] + positive_features[:poscutoff]
# test_set = negative_features[negcutoff:] + positive_features[poscutoff:]


# Try changing from below:
# [BernoulliNB(), MultinomialNB(), LogisticRegression(), SVC(),
#     LinearSVC(), NuSVC()]
classifier = SklearnClassifier(LinearSVC())
classifier.train(train_set)


# classifier = NaiveBayesClassifier.train(train_set)
# print ('accuracy:', nltk.classify.util.accuracy(classifier, test_set))
# classifier.show_most_informative_features()

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

# print('BernoulliNB`s accuracy is %f'  %score(BernoulliNB()))
# print('MultinomiaNB`s accuracy is %f'  %score(MultinomialNB()))
# print('LogisticRegression`s accuracy is  %f' %score(LogisticRegression()))
# print('SVC`s accuracy is %f'  %score(SVC()))
# print('LinearSVC`s accuracy is %f'  %score(LinearSVC()))
# print('NuSVC`s accuracy is %f'  %score(NuSVC()))

# print(positive_features)
# print(negative_features)

# print(pos_words)
# print(neg_words)