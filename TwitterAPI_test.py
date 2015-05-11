#Practice Using Twitter API

#Sources
# https://grahamnic.wordpress.com/2013/09/15/python-using-the-twitter-api-to-datamine/
# http://simpledeveloper.com/twitter-search-api-example/
# http://simpledeveloper.com/how-to-use-python-to-see-what-people-are-saying-about-speaker-john-boehner/

# use the following line to install the python wrapper for the Twitter API
# sudo easy_install python-twitter
import twitter


####################------------------------------------------------####################

# include argparse so that we can just put in the arguments in the command line in terminal 
import argparse

#Top Level
parser = argparse.ArgumentParser(prog='stwitter', description='Custom search of Twitter')
parser.add_argument('-c', '--count', metavar='num', default=100, type=int, help='The total number of tweets to return (before filters)')
parser.add_argument('-f', '--removefilters', action='store_true', help='Removes the tweet filters')
parser.add_argument('-d', '--removedirect', action='store_true', help='Filters direct tweets to our account')
sp = parser.add_subparsers(dest='command')
#Adventure Sub
sp_adventure = sp.add_parser('adventure', help='%(prog)s searches for adventure')
#MyHob Sub
sp_myhob = sp.add_parser('myhob', help='%(prog)s searches for my hobbies')
#Keyword Sub
sp_keyword = sp.add_parser('search', help='%(prog)s searches using a custom query')
sp_keyword.add_argument('term', type=str, help='A query for searching Twitter; must be in quotes')

####################------------------------------------------------####################


#Documentation for Twitter package
# https://code.google.com/p/python-twitter/
# https://dev.twitter.com/overview/documentation
# https://www.apichangelog.com/api/twitter

#Exploring the Twitter API -- API Console
# https://dev.twitter.com/rest/tools/console

# the following gives all the required authorization data to Twitter so they know who we are and we know who they are
api = twitter.Api(
	consumer_key='rdoex8TSB5LYifzEF1xTRTItd',
	consumer_secret='48HfWWfrzh5Z2WgSOVMuQxoqXxzCbEhaucRQs2lHnFfsKR9YAa',
	access_token_key='2875906764-MWh7leZxkOVNcer85k0evxC2nbFwdih2R8eqC4C',
	access_token_secret='kQPldSmsWnSX3rmyS3lUUkZWdL5T0GZZfrfoP6wbd8gWY'
	)
# find all that info here:
# https://apps.twitter.com/

# simple twitter search by using the following code
#search = api.GetSearch(term='adventure', lang='en', result_type='recent', count=100, max_id='')
#for t in search:
#	print t.user.screen_name + ' (' + t.created_at + ')'
#	#Add the .encode to force encoding
#	print t.text.encode('utf-8') + '\n'


####################------------------------------------------------####################


#How to set up Twitter Search
# go to the following link and do a sample search
# https://twitter.com/search
# and follow the query options:
# https://dev.twitter.com/rest/public/search
# note: the format should follow the 'URL encode' syntax:
# http://en.wikipedia.org/wiki/Percent-encoding
# also check out the Get/Search Documentation:
# https://dev.twitter.com/rest/reference/get/search/tweets

# check this link out for Streaming Public Tweets
# https://dev.twitter.com/streaming/public




####################------------------------------------------------####################


#Parse the Args
args = parser.parse_args()
if args.command != '':
#Custom looping so we can search more than 100 tweets
 tweetID = ''
 i = int(round(args.count -51, -2)) / 100 + 1
 for x in range (0, i):

 #Perform Find
 	if args.command == 'adventure':
 		print '------Searching Tweets about adventure ' + str(x * 100) + '/' + str(args.count) + '------'
 		search = api.GetSearch(term='"adventure" OR "space travel" OR "deep sea diving" OR "exploring"', lang='en', result_type='recent', count=(args.count - 100 * x), max_id=tweetID)

 	elif args.command == 'myhob':
 		print '------Searching Tweets about my hobbies ' + str(x * 100) + '/' + str(args.count) + '------'
 		search = api.GetSearch(term='"computers" OR "python" OR "Japanese" OR "Bento"', lang='en', result_type='recent', count=(args.count - 100 * x), max_id=tweetID)

 	elif args.command == 'search':
		print '------Searching Tweets using \"' + args.term + '\"' + str(x * 100) + '/' + str(args.count) + '------'
 		search = api.GetSearch(term=args.term, lang='en', result_type='recent', count=(args.count - 100 * x), max_id=tweetID)

 #Filter Results
 for t in search:
 	#Filter the results by default
 	if args.removefilters == False:
 		if (
 			#Filters Twitter Account
 			t.user.screen_name != 'jerkface' and
 			t.user.screen_name != 'notniceguy' and
 			t.user.screen_name != 'spambot' and
 			t.user.screen_name != 'junkbot' and
 			#Filter Retweets
 			'RT @' not in t.text and
 			#Filter Direct Tweets
 			(args.removedirect == False or '@mytwittername' not in t.text) and
 			#Filter out words
 			'sex' not in t.text):
 				print ''
 				print t.user.screen_name + ' (' + t.created_at + ')'
 				#Add the .encode to force encoding
 				print t.text.encode('utf-8')
 				print ''

 		else:
 			print ''
 			print t.user.screen_name
 			print t.created_at
 			print t.text.encode('utf-8')
 			print ''
		#Save the this tweet ID
		tweetID = t.id