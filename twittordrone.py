#!/usr/bin/env python
#
# TwitterDrone
# PyBorg / Twitter module
#
# pike*2012
#

import os, codecs, sys, re, pickle, twitter
os.chdir(os.path.abspath(os.path.dirname(sys.argv[0])))
sys.path.append( "./pyborg" )
from pyborg import pyborg

#-- settings


# get your keys at dev.twitter.com
CKEY	= 'aaaa'
CSECRET	= 'bbbb'
AKEY	= 'cccc'
ASECRET	= 'dddd'

newsuser="cnn"
doDebug=False

doPublic=True
doFriends=True
doFollowers=True
doReplies=True
doNews=True
dontReplyPublic=False
dontReplyFriends=False
dontReplyFollowers=False
dontReplyReplies=False
dontReplyNews=False

doDirectMessages=True
dontAddressPeople=False

#-- / settings


sys.stdout = codecs.getwriter('utf8')(sys.stdout)

if __name__ == "__main__":

	try:
		twistoryfile = open("tweets.pck", "r") 
		twistorydict = pickle.load(twistoryfile)
		twistoryfile.close()
	except IOError:
		twistorydict = {"@me":"alive"}
		twistoryfile = open("tweets.pck", "w") 
		pickle.dump(twistorydict, twistoryfile)
		twistoryfile.close()

	
	
	pybot		= pyborg.pyborg()
	api 		= twitter.Api(consumer_key=CKEY, consumer_secret=CSECRET, access_token_key=AKEY, access_token_secret=ASECRET)
	me		= api.VerifyCredentials()
	replytweets	= {}
	
	#print twistorydict

	
	if doPublic:
		print
		print "---------- doPublic"
		#learn some public stauff
		try:
			tweets = api.GetPublicTimeline()
		except Exception:
			print "-- couldnt get public tweets"
			tweets = []
			
		for tweet in tweets:
			print "-- public"
			print tweet.text
			if not dontReplyPublic:
				replytweets[tweet.GetCreatedAtInSeconds()]=tweet.text
			cleantweet = pyborg.filter_message(tweet.text)
			pybot.learn(cleantweet)
			
			
	if doFriends:
		print
		print "---------- doFriends"
		# learns my friends words
		try:
			tweets = api.GetFriendsTimeline()
		except Exception:
			print "-- couldnt get tweets from friends"
			tweets = []
			
		for tweet in tweets:
			if tweet.user.screen_name!=me.screen_name:
				print "-- friends"
				print tweet.text
				if not dontReplyFriends:
					replytweets[tweet.GetCreatedAtInSeconds()]=tweet.text
				cleantweet = pyborg.filter_message(tweet.text)
				pybot.learn(cleantweet)
				
			else:
				print "-- ignoring my own tweet"
		
	if doFollowers:	
		print
		print "---------- doFollowers"
		# learn my followers
		try:
			followers = api.GetFollowers()
		except Exception:
			print "-- couldnt get tweets from followers"
			followers = []
			
		for follower in followers:
			try:
				tweets = api.GetUserTimeline(follower.id)
			except Exception:
				print "-- couldnt get tweets from %s"%follower.name
				tweets=[]
				
			for tweet in tweets:
				print "-- follower %s"%follower.name
				print tweet.text
				if not dontReplyFollowers:
					replytweets[tweet.GetCreatedAtInSeconds()]=tweet.text
				cleantweet = pyborg.filter_message(tweet.text)
				pybot.learn(cleantweet)
				
	
	if doReplies:
		# replies are replied instantly
		print
		print "---------- doReplies"
		# check @ replies
		# prepend @sender: to the tweet
		try:
			tweets = api.GetReplies()
		except Exception:
			print "-- couldnt get @replies"
			tweets = []
			
		for tweet in tweets:
			if tweet.user.screen_name!=me.screen_name:
				print "-- @reply"
				# replace @me with @him
				orgtweet = tweet.text
				#strippedtweet = orgtweet[len(me.screen_name)+1:]
				#bouncetweet = "@%s %s"%(tweet.user.screen_name,strippedtweet)
				strippedtweet = orgtweet.replace('@'+me.screen_name,"")
				print orgtweet
				if not dontReplyReplies:
					#replytweets[tweet.GetCreatedAtInSeconds()]=bouncetweet
					if twistorydict.has_key(orgtweet):
						print "already replied to %s"%orgtweet
					else:
						# reply to the clean version, prefix his name
						replytweet = pybot.reply(strippedtweet)
						replytweet = "@%s %s"%(tweet.user.screen_name,replytweet)
						#print "in reply to: %s"%tweet
						print "sending reply: %s"%replytweet
						twistorydict[orgtweet]=replytweet
						if not doDebug:
							try:
								status = api.PostUpdate(replytweet)
							except Exception:
								print "-- couldnt post @reply"
							
				cleantweet = pyborg.filter_message(strippedtweet)
				pybot.learn(cleantweet)
				
			else:
				print "-- ignoring my own tweet"

	if doNews:
		# news is replied instantly
		print
		print "---------- doNews"
		# check news tweets
		try:
			tweets = api.GetUserTimeline(newsuser)
		except Exception:
			print "-- couldnt get news"
			tweets = []
			
		if len(tweets):
			tweet = tweets[0]
			if tweet.user.screen_name!=me.screen_name:
				print "-- news"
				orgtweet = tweet.text
				print orgtweet
				if not dontReplyNews:
					if twistorydict.has_key(orgtweet):
						print "already replied to %s"%orgtweet
					else:
						# reply to the clean version, prefix his name
						replytweet = pybot.reply(orgtweet)
						print "sending reply: %s"%replytweet
						twistorydict[orgtweet]=replytweet
						if not doDebug:
							try:
								status = api.PostUpdate(replytweet)
							except Exception:
								print "-- couldnt post @reply"
							
				cleantweet = pyborg.filter_message(orgtweet)
				pybot.learn(cleantweet)
				
			else:
				print "-- ignoring my own tweet"
			
	pybot.save_all()
	
	if len(replytweets):
		print
		print "---------- random tweet"
	
		# reply to the last tweet in all tweets found
		tweettimes		= replytweets.keys()
		tweettimes.sort()
	
		# find the latest tweet we havent
		# already replied to 
		lasttweet="@me"
		while twistorydict.has_key(lasttweet):
			print "skipping one, already replied to %s"%lasttweet
			lasttweettime 	= tweettimes.pop()
			lasttweet 		= replytweets[lasttweettime]
	
		print "-- lasttweet %s"%lasttweettime
		
		# see if it was a reply and reform it
		splittweet = re.split('^ *(@\w+) *', lasttweet, 1)
		if len(splittweet)==3:
			replyto = splittweet[1]
			lasttweet = splittweet[2]
			print "in reply to %s"%replyto
		else:
			replyto = ""
		
		print "-- tweet based on"
		print lasttweet
		bottweet = pybot.reply(lasttweet)
	
		
		if dontAddressPeople:
			print "-- removing all @reply"
			bottweet = "".join(re.split('@\w+', bottweet))
		
		if replyto!="":
			print "-- replying: removing any prefix @reply from original message"
			print bottweet
			bottweet = "".join(re.split('^@\w+', bottweet))
			print "-- prefixing %s"%replyto
			bottweet = "%s %s"%(replyto,bottweet)
		
		print "-- posting final bottweet:"
		print bottweet
	
		# -- post the tweet !
		twistorydict[lasttweet]=bottweet
		if not doDebug:
			try:
				status = api.PostUpdate(bottweet)
			except Exception:
				print "-- couldnt post bottweet"
		
	else:
		print "-- no tweets to reply to ?"
		
	if doDirectMessages:
	
		print
		print "---------- doDirectMessages"
		# ------- direct messages

		try:
			dms = api.GetDirectMessages()
		except Exception:
			print "-- couldnt get DM"
			dms = []
			
		for dm in dms:
			if dm.sender_screen_name!=me.screen_name:
				print "-- DM %s"%dm.sender_screen_name
				print dm.text
				cleandm = pyborg.filter_message(dm.text)
				pybot.learn(cleandm)
				
				#reply
				print "-- replying to DM"
				reply = pybot.reply(dm.text)
				print "-- sending DM reply:"
				print reply
				if not doDebug:
					try:
						status = api.PostDirectMessage(dm.sender_id,reply)
						api.DestroyDirectMessage(dm.id)
					except Exception:
						print "-- couldnt send DM reply"
			else:
				print "-- ignoring my own dm"
				
			pybot.save_all()	
		
	print
	print "---------- Done"
	print "-- saving previously replied tweets"
	
	twistoryfile = open("tweets.pck", "w") 
	pickle.dump(twistorydict, twistoryfile)
	twistoryfile.close()
		
# done
	