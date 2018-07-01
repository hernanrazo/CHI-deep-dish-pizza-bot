import praw
import tweepy
from textblob import TextBlob 

#Set averages and counter to zero
#Declare empty lists for storing subjectivity and polarity values
polarity_list = []
subjectivity_list = []
polarity_avg = 0
subjectivity_avg = 0
polarity_sum = 0
subjectivity_sum = 0
counter = 0

#Twitter API credentials
consumer_key = 'YOUR KEY HERE'
consumer_secret = 'YOUR SECRET HERE'
access_token = 'YOUR TOKEN HERE'
access_token_secret = 'YOUT TOKEN SECRET HERE'

#Use twitter credentials to access tweets
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#Enter string that should be searched for in tweets
public_tweets = api.search('chicago deep dish')

#Reddit API credentials
reddit = praw.Reddit(client_id = 'YOUR CLIENT ID HERE', 
				     client_secret = 'YOUR CLIENT SECRET HERE', 
					 username = 'YOUR USERNAME HERE', 
			 	 	 password = 'YOUR PASSWORD HERE', 
					 user_agent = 'YOUR USER AGENT HERE')

#Declare which subreddit to be active on
subreddit = reddit.subreddit('chicago')

#Declare keyphrase to activate bot
keyphrase = 'chicago deep dish'

#Search through first 100 public tweets
#append polarity and subjectivity values onto lists
while (counter < 100):
	for tweet in public_tweets:

		subjectivity = TextBlob(tweet.text).sentiment.subjectivity
		polarity = TextBlob(tweet.text).sentiment.polarity
		subjectivity_list.append(subjectivity)
		polarity_list.append(polarity)
		counter += 1

#find subjectivity average
for num in subjectivity_list:

	subjectivity_sum += num
	subjectivity_avg = subjectivity_sum / len(subjectivity_list)

#find polarity average
for num in polarity_list:

	polarity_sum += num
	polarity_avg = polarity_sum / len(polarity_list)
	
#Search for keyphrase in reddit comments 
for comment in subreddit.stream.comments():

	#if phrase found, print the response
	try:
		if keyphrase in comment.body:
		
			comment.reply('It looks like you mentioned Chicago\'s famous deep dish pizza! ' +
				'On Twitter, deep dish pizza has an average subjectivity value of ' +
				str(subjectivity_avg) + ' and an average polarity value of ' +
				str(polarity_avg) + '.')

			print('Commented successfully.')

		else:
			print('Did not comment.')

	except:
		print('Error when tried to reply.')
