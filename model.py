import re
import tweepy
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from tweepy import OAuthHandler
from textblob import TextBlob

class TwitterClient(object):
	#connecting to twitter API
	def __init__(self):
		#constructor
		consumer_key = 'hErizb29LAeLUUms8izUTozHz'
		consumer_secret = 'IgOq53bGtfCOJrQYxGjTa7LqHCWdgs5y1YcjKzKa5VKFbwTsvb'
		access_token = '773659966267875328-V4Tb1swk6jEpmHvWQCxcehyvz1lVDkd'
		access_token_secret = 'G0nP4RhIQPTVo63vD2o6zSkye9UPoOHQLMtU74mEgAhtk'

		#attempt authentication
		try:
			self.auth = OAuthHandler(consumer_key, consumer_secret)
			self.auth.set_access_token(access_token, access_token_secret)
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

def main():
	api = TwitterClient()
	user_name = 'realDonaldTrump';
	tweets, dates = api.get_tweets(user = user_name, count = 1000)
	print("Number of Tweets: {}".format(len(tweets)))
	
	#Sort positive, neutral, and negative tweets
	pos_tweets = [tweet for tweet in tweets if tweet > 0]
	print("Positive tweets percentage: {} %".format(100*len(pos_tweets)/len(tweets)))
	neg_tweets = [tweet for tweet in tweets if tweet < 0]
	print("Negative tweets percentage: {} %".format(100*len(neg_tweets)/len(tweets)))
	neutral_tweets = [tweet for tweet in tweets if tweet == 0]
	print("Neutral tweets percentage: {} %".format(100*len(neutral_tweets)/len(tweets)))

	for date in dates[:10]:
		print(date)
	
	dates = [pd.to_datetime(d) for d in dates]
	plt.scatter(dates, tweets, s =50, c = 'red')
	plt.show()

if __name__ == "__main__":
	main()











