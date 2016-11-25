#Copyright 2016 Robbie MacGregor

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os
import tweepy
from random import randint
from time import gmtime, strftime, sleep, time
from secrets import *
from sentences import *

#Twitter authentication
auth = tweepy.OAuthHandler(API_Key, API_Secret)
auth.set_access_token(Access_Token, Access_Token_Secret)
api = tweepy.API(auth)

#Set up logging
bot_username = 'ELHTOOracle'
logfile_name = bot_username + '.log'

#Log tweets
def log(tweet):
    path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(path, logfile_name), 'a+') as log_file:
        current_time = strftime('%d %b %Y %H:%M:%S', gmtime())
        log_file.write('\n' + current_time + ' ' + tweet)

# Send the tweet and log success or failure
def tweet(text):
    try:
        api.update_status(text)
    except:
        log(tweepy.error.TweepError.message)
    else:
        log('Tweeted: ' + text)

hash = '#ELHTO'
fresh = range(len(sentences))

#This is where the magic happens
def tweet_fortunes():
    if len(fresh) > 0:
        pick = fresh.pop(randint(0, len(fresh)-1))
        fortune = sentences[pick]
        if len(fortune) == 1:
            tweet(fortune[0] + ' ' + hash)
        else:
            for phrase in fortune:
                if fortune.index(phrase) != (len(fortune) -1):
                    tweet(phrase)
                    sleep(45)
                else:
                    tweet(phrase + ' ' + hash)
        sleep(300)
    else:
        pick = randint(0, len(sentences)-1)
        fortune = sentences[pick]
        if len(fortune) == 1:
            tweet(fortune[0] + ' ' + hash)
        else:
            for phrase in fortune:
                if fortune.index(phrase) != (len(fortune) -1):
                    tweet(phrase)
                    sleep(45)
                else:
                    tweet(phrase + ' ' + hash)
        fresh = range(len(sentences))
        fresh.pop(pick)
        sleep(300)

#Find followers and follow them back
def follow_back():
    for follower in api.followers():
        api.create_friendship(follower.id)

#Send a greeting to new followers via direct message,
#checking to ensure they've not already been greeted.
def greet():
    greeted = [message.recipient.id for message in api.sent_direct_messages()]
    for follower in api.followers():
        if follower.id not in greeted:
            api.send_direct_message(follower.id, text = 'Hi! Thanks for following me. I\'m going to tweet a fortune for you in about 10 minutes, unless you message me back and say "NO THANKS.".')

#Check to see if followers who have been greeted have declined a fortune.
def check():
    greeted = [message.recipient.id for message in api.sent_direct_messages()]
    responded = [message.sender.id for message in api.direct_messages()]
    for follower in api.followers():
        if follower.id in greeted:
            if follower.id in responded:
                # regex check for 'no thanks' in message and follower.id not in tweeted file
                    # tweet fortune at follower
                    # add @handle to tweeted file
                    # sleep(600)
                print message




#follow_back()
# greet()
check()
#tweet_fortunes()
