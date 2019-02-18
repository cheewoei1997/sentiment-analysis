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

nltk.download('punkt')


# from analyser import set_data


class SentimentForm(Form):
    sentence = TextField('Type your sentence here', validators=[Required()])
    classifier = RadioField('This is a radio field', choices=[
        ('bernb', 'BernoulliNB'),
        ('multi', 'Multinomial'),
        ('logreg', 'Logistic Regression'),
        ('svc', 'SVC'),
        ('lsvc', 'LinearSVC'),
    ])

    submit_button = SubmitField('Submit')


def create_app(configfile=None):
    app = Flask(__name__)
    AppConfig(app, configfile)  # Flask-Appconfig is not necessary, but
                                # highly recommend =)
                                # https://github.com/mbr/flask-appconfig
    Bootstrap(app)

    # in a real app, these should be configured through Flask-Appconfig
    app.config['SECRET_KEY'] = 'devkey'
    app.config['RECAPTCHA_PUBLIC_KEY'] = \
        '6Lfol9cSAAAAADAkodaYl9wvQCwBMr3qGR_PPHcw'

    
    @app.route('/', methods=('GET', 'POST'))
    def index():
        # form = ExampleForm()
        form = SentimentForm()
        form.validate_on_submit()  # to get error messages to the browser
        # flash('critical message', 'critical')
        # flash('error message', 'error')
        # flash('warning message', 'warning')
        # flash('info message', 'info')
        # flash('debug message', 'debug')
        # flash('different message', 'different')
        # flash('uncategorized message')

        if form.validate_on_submit():
            if request.method == 'POST':
                result = request.form
                input_sentence = set_data(result)
                train_data = get_dataset(input_sentence)

                choice = result['classifier']
                choice_dict = {
                    'bernb': 'Bernoulli Naive Bayes',
                    'multi': 'Multinomial Naive Bayes',
                    'logreg': 'Logistic Regression',
                    'svc': 'Support Vector Classifier',
                    'lsvc': 'Linear Support Vector Classifier',
                }

                if choice == 'bernb':
                    stats = set_classifier(BernoulliNB(), train_data, input_sentence)
                elif choice == 'multi':
                    stats = set_classifier(MultinomialNB(), train_data, input_sentence)
                elif choice == 'logreg':
                    stats = set_classifier(LogisticRegression(), train_data, input_sentence)
                elif choice == 'svc':
                    stats = set_classifier(SVC(), train_data, input_sentence)
                elif choice == 'lsvc':
                    stats = set_classifier(LinearSVC(), train_data, input_sentence)
                else:
                    print('Something went terribly wrong')

                stats_dict = {
                    'posPercent': stats[0],
                    'negPercent': stats[1],
                    'pos': stats[2],
                    'neg': stats[3],
                    'sentence': result['sentence'],
                    'train_data': train_data,
                    'choice': choice_dict[str(choice)],
                }

                return render_template('result.html', context=stats_dict)
            
            else:
                print('ELSEEEE')
                print(request.form)
                # print(form.csrf_token)
                return render_template('error.html', form=form)     

        return render_template('index.html', form=form)


    # @app.route('/result/')
    # def result():
    #     print('Hola this is result')
    #     return render_template('result.html')


    return app


def word_feats(words):
    return dict([(words, True)])


def set_data(requested):
    sentence = requested['sentence']
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

    # Keep both positive and negative into posneg
    posneg = pos_words + neg_words

    neu_words = []
    [neu_words.append(neu) for neu in target if neu not in posneg]

    positive_features = [(word_feats(pos), 'pos') for pos in pos_words]
    negative_features = [(word_feats(neg), 'neg') for neg in neg_words]
    neutral_features = [(word_feats(neu.lower()), 'neu') for neu in neu_words]

    shuffle(negative_features)
    negative_features = negative_features[:len(positive_features)]
    print('Positive feats:', len(positive_features))
    print('Negative feats:', len(negative_features))
    print('Neutral feats:', neutral_features)

    train_set = positive_features + negative_features + neutral_features
    return train_set


def set_classifier(chosen_classifier, train_set, sentence):
    classifier = SklearnClassifier(chosen_classifier)
    classifier.train(train_set)

    neg = 0
    pos = 0
    print('set_classifier', sentence)

    for word in sentence:
        classResult = classifier.classify(word_feats(word))
        print(word_feats(word))
        print(classResult)
        if classResult == 'neg':
            neg = neg + 1
        if classResult == 'pos':
            pos = pos + 1

    posPercent = str(float(pos)/len(sentence))
    negPercent = str(float(neg)/len(sentence))
    
    # print ('Accuracy:', nltk.classify.util.accuracy(classifier, sentence))
    classifier.show_most_informative_features()
    # print('Score:', score)

    print('Positive: ' + posPercent)
    print('Negative: ' + negPercent)
    print('Pos', pos)
    print('Neg', neg)

    return posPercent, negPercent, pos, neg
        

if __name__ == '__main__':
    create_app().run(debug=True)
