#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv

#Credentials to login to twitter api
consumer_key = '0JOGbCd8iEqvK3clmM0ygFHIl'
consumer_secret = 'FO3wKwijIELJRZcErsEazBDB6O8GnEuaZhJgXqaJKIF18VhVmE'

#Set Access Tokens
access_token = '1167807025-g47ctxV1ZNesoJVBzqWXIcg6lu1pJWw80xaNoMr'
access_secret = 'eysD8CMYwXMUFHF3JEl1Hgbr5UkgUEUTrtIACz77NYkjy'


def get_tweets(interest):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	

	#Get all of the users to search from a csv
	screen_names = []
	with open('%s_users.csv' % interest, 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			screen_names.append(row[0])

	#Just ensuring that the list was made
	print("Last user in the list: " + str(screen_names[-1]))

	#Loop every user in the list
	for screen_name in screen_names:
		print("Grabbing tweets from %s"%screen_name)
		#make initial request for most recent tweets (200 is the maximum allowed count)
		try:
			new_tweets = api.user_timeline(screen_name = screen_name,count=200)
		except tweepy.TweepError:
			print("Failed to run the command on %s, Skipping..."%screen_name)
		
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#save the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		#keep grabbing tweets until there are no tweets left to grab
		while len(new_tweets) > 0:

			#all subsequent requests use the max_id param to prevent duplicates
			new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
			
			
			#save most recent tweets
			alltweets.extend(new_tweets)
			
			#update the id of the oldest tweet less one
			oldest = alltweets[-1].id - 1
			
			
			print "...%s tweets downloaded so far...%s" % (len(alltweets), screen_name)
		
		#transform the tweepy tweets into a 2D array that will populate the csv	
		outtweets = [[tweet.id_str, tweet.user.screen_name, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
	print("\nGrabbed all of the tweets!")
	
	
	
	#write the csv	
	with open('%s_tweets.csv' % interest, 'a') as f:
		writer = csv.writer(f)
		writer.writerows(outtweets)
	
	pass


def initialize_interest():
	interest = raw_input("\nGive your category of tweets\n")
	try:
		with open('%s_tweets.csv' % (interest), 'r') as f:
			reader = csv.reader(f)
	except IOError as e:
		print("\nLooks like you need to create a new interest category...")
		with open('%s_tweets.csv' % (interest), 'wb') as f:
			writer = csv.writer(f)
			writer.writerow(["id", "user", "created_at","text"])
			print("CSV file created for %s tweets" % (interest))
			initialize_users(interest)
		
	return interest
	

def read_tweets():
	interest = raw_input("\nWhat is the interest you are searching tweets for?\n")
	with open('%s_tweets.csv' % interest) as f:
		reader = csv.reader(f)
		num = raw_input("\nHow many tweets would you like to read?\n")
		num = int(num)
		for row in reader:
			if(num==0):
				break
			print row[3]
			num = num-1
				

def initialize_users(interest):
	with open('%s_users.csv' % interest, 'wb') as f:
			writer = csv.writer(f)
			user = raw_input("\nYou also need to initialize some users that you would like to grab tweet data from.\nType in one twitter handle at a time to keep appending to the list of users.\nIf at any time you would like to end the list then just type the word 'quit'.\n>")
			while(user!="quit"):
				writer.writerow([user])
				user = raw_input(">")
			print("CSV file created for %s users\n" % interest)

if __name__ == '__main__':
	print("Welcome to Tyler Bedford's Tweet Gathering Console Application!")
	while(1):
		input = raw_input("\nWhat would you like to do?\n")

		if(input=="getTweets"):
			interest = initialize_interest()
			get_tweets(interest)

		elif(input=="readTweets"):
			read_tweets()

		elif(input=="quit"):
			print("\nThanks for using my app! Hope you enjoyed!\n")
			break
		
		else:
			print("\nSorry, I don't know what command that is. The list of usable commands are located in the READ.ME")

	
	
