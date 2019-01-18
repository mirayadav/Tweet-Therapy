import re
import tweepy
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt, mpld3
import numpy as np
import datetime as dt
import base64
import config
from io import BytesIO
from tweepy import OAuthHandler
from textblob import TextBlob
from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/graph/', methods=['POST', 'GET'])
def graph():
	if request.method == 'POST':
		text1 = request.form['text1']
		results, pos, neg, neutral = generate_graph(text1)
		tot = 100-pos-neg-neutral
		neutral = neutral+tot
		title = "@" + text1 + "'s Mood Analyzed From Tweets"
		return render_template('graph.html', name=title, url = results, p = pos, n = neg, t = neutral)

class TwitterClient(object):
	#connecting to twitter API
	def __init__(self):
		#attempt authentication
		try:
			self.auth = OAuthHandler(config.consumer_key, config.consumer_secret)
			self.auth.set_access_token(config.access_token, config.access_token_secret)
			self.api = tweepy.API(self.auth)

		except:
			print("Error: Authentication Failed")

	def clean_tweet(self,tweet):
		#removes links and special characters
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

	def get_tweet_sentiment(self,tweet):
		#classify sentiment using TextBlob
		analysis = TextBlob(self.clean_tweet(tweet))
		return analysis.sentiment.polarity

	def get_tweets(self, user, count= 2000):
		#get and parse tweets 
		tweets = []
		dates = []
		no_of_pages = 15
		for i in xrange(no_of_pages):
			try:
				fetched_tweets = self.api.user_timeline(screen_name = user, page = i)
				for tweet in fetched_tweets:
					parsed_tweet = {}
					if tweet.retweet_count > 0:
						if parsed_tweet not in tweets:
							tweets.append(self.get_tweet_sentiment(tweet.text))
							dates.append(tweet.created_at)
					else:
						tweets.append(self.get_tweet_sentiment(tweet.text))
						dates.append(tweet.created_at)

			except tweepy.TweepError as e:
				print("Error: " + str(e))

		return tweets, dates

def generate_graph(user_name = " "):
	api = TwitterClient()
	tweets, dates = api.get_tweets(user = user_name, count = 1000)
	print("Number of Tweets: {}".format(len(tweets)))
	
	#Sort positive, neutral, and negative tweets
	pos_tweets = [tweet for tweet in tweets if tweet > 0]
	pos_tweet_percentage = 100*len(pos_tweets)/len(tweets)
	neg_tweets = [tweet for tweet in tweets if tweet < 0]
	neg_tweet_percentage = 100*len(neg_tweets)/len(tweets)
	neutral_tweets = [tweet for tweet in tweets if tweet == 0]
	neutral_tweet_percentage = 100*len(neutral_tweets)/len(tweets)


	dates = [pd.to_datetime(d) for d in dates]

	plt.figure(figsize=(10,6))
	plt.scatter(dates, tweets, c=tweets)
	plt.xlabel('Tweet Date')
	plt.ylabel('Mood')
	#plt.title("@" + user_name + "'s Mood in Tweets")
	figfile = BytesIO()
	plt.savefig(figfile, format='png')
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	
	return figdata_png, pos_tweet_percentage, neg_tweet_percentage, neutral_tweet_percentage


if __name__ == "__main__":
    app.run(debug=True)











