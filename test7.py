from flask import Flask, render_template, flash, request
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig
from flask_wtf import Form, RecaptchaField
from flask_wtf.file import FileField
from wtforms import TextField, HiddenField, ValidationError, RadioField,\
    BooleanField, SubmitField, IntegerField, FormField, validators
from wtforms.validators import Required

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
from random import shuffle

bstats = []
mstats = []
lstats = []
sstats = []
vstats = []

def word_feats(words):
    return dict([(words, True)])


def set_data(requested):
    sentence = requested
    target = sentence.lower()
    target = nltk.word_tokenize(target)
    return target


def get_dataset(target):
    # Loads the positive and negative words
    pos_words = open(os.path.join('datasets', 'positive-words.txt'), 'r').read()
    neg_words = open(os.path.join('datasets', 'negative-words.txt'), 'r').read()

    # Tokenize the words
    pos_words = nltk.word_tokenize(pos_words)
    neg_words = nltk.word_tokenize(neg_words)
    shuffle(pos_words)
    shuffle(neg_words)
    neg_words = neg_words[:2139]

    # Keep both positive and negative into posneg
    posneg = pos_words + neg_words

    neu_words = []
    [neu_words.append(neu) for neu in target if neu not in posneg]

    positive_features = [(word_feats(pos), 'pos') for pos in pos_words]
    negative_features = [(word_feats(neg), 'neg') for neg in neg_words]
    neutral_features = [(word_feats(neu.lower()), 'neu') for neu in neu_words]

    # print('Positive feats:', len(positive_features))
    # print('Negative feats:', len(negative_features))
    # print('Neutral feats:', neutral_features)

    train_set = positive_features + negative_features + neutral_features
    return train_set


def set_classifier(chosen_classifier, train_set, sentence):
    classifier = SklearnClassifier(chosen_classifier)
    classifier.train(train_set)

    neg = 0
    pos = 0
    # print('Classifier:', str(chosen_classifier))

    for word in sentence:
        classResult = classifier.classify(word_feats(word))
        # print(word_feats(word))
        # print(classResult)
        if classResult == 'neg':
            neg = neg + 1
        if classResult == 'pos':
            pos = pos + 1

    posPercent = str(float(pos)/len(sentence))
    negPercent = str(float(neg)/len(sentence))
    
    # print ('Accuracy:', nltk.classify.util.accuracy(classifier, sentence))
    # classifier.show_most_informative_features()
    # print('Score:', score)

    # print('Positive: ' + posPercent)
    # print('Negative: ' + negPercent)
    # print('Pos', pos)
    # print('Neg', neg)

    return posPercent, negPercent, pos, neg


sentences = ['the show is not only great, but also fantastic and a masterpiece',
            'today is definitely a day for walking the dog',
            'i love how the movie managed to capture my attention throughout the 2 hour span',
            'great comment! i fully support your actions, as they resonate well with mine',
            'show is really funny, and i adore it',
            'i love the main character and his shenanigans',
            'i really like how the show speaks to its viewers',
            'it speaks volumes about how a single episode can so beautifully portray the mind of an animal',
            'a really great movie, nothing much to say apart that i absolutely it!',
            'Great fun. I wouldd watch it again with my daughter.',
            'Stop these movies, they are just the most vile of all facets of our society. Please. Stop. NOW.',
            'It was just not my cup of tea.',
            'The film, to put it even more bluntly, is a total bore and would appeal to no one but perhaps those who made the film',
            'I would write this off as another lousy film.',
            'you can tell other people how you couldn not believe how terrible the movie was.',
            'The music is awful and totally out of place, and the whole thing looks and sounds like a poor school play.',
            'although the plot was OK, I found the film to be a bore and over dramatic.',
            'I give it 1 out of 10, truly one of the worst 20 movies for its budget level that I have ever seen',
            'horrible show, i did not expect that ending and believe that the rest of your audience feels the same way',]
    
# switch out request.form with the 20 sentences
# result = request.form
for result in sentences:
    # print(result)
    input_sentence = set_data(result)
    input_sentence = set_data(result)
    train_data = get_dataset(input_sentence)

    # choice = result['classifier']
    choice_dict = {
        'bernb': 'Bernoulli Naive Bayes',
        'multi': 'Multinomial Naive Bayes',
        'logreg': 'Logistic Regression',
        'svc': 'Support Vector Classifier',
        'lsvc': 'Linear Support Vector Classifier',
    }

    print('='*80)
    print('Bernoulli')
    print(set_classifier(BernoulliNB(), train_data, input_sentence))
    print('='*80)
    print('Multinomial')
    print(set_classifier(MultinomialNB(), train_data, input_sentence))
    print('='*80)
    print('LogisticRegression')
    print(set_classifier(LogisticRegression(), train_data, input_sentence))
    print('='*80)
    print('SVC')
    print(set_classifier(SVC(), train_data, input_sentence))
    print('='*80)
    print('LinearSVC')
    print(set_classifier(LinearSVC(), train_data, input_sentence))

    bstats.append(set_classifier(BernoulliNB(), train_data, input_sentence))
    mstats.append(set_classifier(MultinomialNB(), train_data, input_sentence))
    lstats.append(set_classifier(LogisticRegression(), train_data, input_sentence))
    sstats.append(set_classifier(SVC(), train_data, input_sentence))
    vstats.append(set_classifier(LinearSVC(), train_data, input_sentence))


# print(bstats)
# print(mstats)
# print(sstats)
# print(sstats)
# print(vstats)

avbstats = [0.000, 0.000, 0, 0]
avmstats = [0.000, 0.000, 0, 0]
avlstats = [0.000, 0.000, 0, 0]
avsstats = [0.000, 0.000, 0, 0]
avvstats = [0.000, 0.000, 0, 0]

somerandom = 0

for stats in bstats:
    avbstats[0] += float(stats[0])
    avbstats[1] += float(stats[1])
    avbstats[2] += int(stats[2])
    avbstats[3] += int(stats[3])
    print(stats)

for stats in mstats:
    avmstats[0] += float(stats[0])
    avmstats[1] += float(stats[1])
    avmstats[2] += int(stats[2])
    avmstats[3] += int(stats[3])
    print(stats)

for stats in lstats:
    avlstats[0] += float(stats[0])
    avlstats[1] += float(stats[1])
    avlstats[2] += int(stats[2])
    avlstats[3] += int(stats[3])
    print(stats)

for stats in sstats:
    avsstats[0] += float(stats[0])
    avsstats[1] += float(stats[1])
    avsstats[2] += int(stats[2])
    avsstats[3] += int(stats[3])
    print(stats)

for stats in vstats:
    avvstats[0] += float(stats[0])
    avvstats[1] += float(stats[1])
    avvstats[2] += int(stats[2])
    avvstats[3] += int(stats[3])
    print(stats)

# divisor = [2, 2, 2, 2]

count = 0
for x in avbstats:
    x = x/2
    avbstats[count] = x
    count += 1

count = 0
for x in avmstats:
    x = x/2
    avmstats[count] = x
    count += 1

count = 0
for x in avlstats:
    x = x/2
    avlstats[count] = x
    count += 1

count = 0
for x in avsstats:
    x = x/2
    avsstats[count] = x
    count += 1

count = 0
for x in avvstats:
    x = x/2
    avvstats[count] = x
    count += 1

print('='*80)
print('B:', avbstats)
print('='*80)
print('M:', avmstats)
print('='*80)
print('L:', avlstats)
print('='*80)
print('S:', avsstats)
print('='*80)
print('V:', avvstats)
# print(avbstats)
# print('Average pos percentage:', b)


# print('Average    {}  {}  {}  {}'.format('posP', 'negP', 'noP', 'noN'))
# print('Bernoulli: {}  {}  {}  {}'.format(bstats.))