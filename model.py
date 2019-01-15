import re
import tweepy
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
		if analysis.sentiment.polarity > 0:
			return 'positive'
		elif analysis.sentiment.polarity == 0:
			return 'neutral'
		else:
			return 'negative'

	def get_tweets(self, query, count = 50):
		#get and parse tweets 
		tweets = []
		
		try:
			fetched_tweets = self.api.search(q = query, count = count)
			for tweet in fetched_tweets:
				parsed_tweet = {}
				parsed_tweet['text'] = tweet.text
				parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
				if tweet.retweet_count > 0:
					if parsed_tweet not in tweets:
						tweets.append(parsed_tweet)
				else:
					tweets.append(parsed_tweet)
			return tweets

		except tweepy.TweepError as e:
			print("Error: " + str(e))

def main():
	api = TwitterClient()
	user_name = 'Donald Trump';
	tweets = api.get_tweets(query = user_name, count = 200)
	
	#Sort positive, neutral, and negative tweets
	pos_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
	print("Positive tweets percentage: {} %".format(100*len(pos_tweets)/len(tweets)))
	neg_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
	print("Negative tweets percentage: {} %".format(100*len(neg_tweets)/len(tweets)))
	neutral_tweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neutral']
	print("Neutral tweets percentage: {} %".format(100*len(neutral_tweets)/len(tweets)))
	

	print("\n\nPositive tweets:")
	for tweet in pos_tweets[:10]:
		print(tweet['text'])
	print("\n\nNegative tweets:")
	for tweet in neg_tweets[:10]:
		print(tweet['text'])
	print("\n\nNeutral tweets:")
	for tweet in neutral_tweets[:10]:
		print(tweet['text'])

if __name__ == "__main__":
	main()











