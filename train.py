import pandas as pd
import matplotlib.pyplot as plt, mpld3
import numpy as np
import sys
import scipy
import sklearn
import nltk


cols = ['sentiment', 'id', 'date', 'query_string', 'user', 'text']
df = pd.read_csv("./trainingandtestdata/training.1600000.processed.noemoticon.csv",header=None, names=cols)
df.head()

df.drop(['id', 'date', 'query_string', 'user'],axis=1,inplace=True)
tweets = []
for (words, sentiment) in df:
	words_filtered = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet.text).split())
	tweets.append((words_filtered, sentiment))

words_features = get_word_features(get_words_in_tweets(tweets))

def get_words_in_tweets(tweets):
	all_words = []
	for (words, sentiment) in tweets:
		all_words.extend(words)
	return all_words

def get_word_features(wordlist):
	worldlist = nltk.FreqDist(wordlist)
	word_features = wordlist.keys()
	return word_features

def extract_features(document):
	document_words = set (document)
	features = {}
	for word in word_features:
		features['contains(%s)' % word] = (word in document_words)
	return features

training_set = nltkclassify.apply_features(extract_features, tweets)
classifier = nltk.NaiveBayesClassifier.train(training_set)



