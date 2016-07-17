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
from secrets import *
from time import gmtime, strftime, sleep, time

#Twitter authentication
auth = tweepy.OAuthHandler(API_Key, API_Secret)  
auth.set_access_token(Access_Token, Access_Token_Secret)  
api = tweepy.API(auth) 

#Set up logging
bot_username = 'ELHTOOracle'
logfile_name = bot_username + '.log'

# Send the tweet and log success or failure
def tweet(text):
    try:
        api.update_status(text)
    except:
        log(tweepy.error.TweepError.message)
    else:
        log('Tweeted: ' + text)

#Log tweets
def log(tweet):
    path = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(path, logfile_name), 'a+') as log_file:
        current_time = strftime('%d %b %Y %H:%M:%S', gmtime())
        log_file.write('\n' + current_time + ' ' + tweet)


#Just a list of test sentences. Still have to write a few lines to parse the text file from the publisher.
sentences = [
['1/3 People face disappointment when things don’t turn out as expected.',
'2/3 You can’t have everything you dream for.',
'3/3 High hopes. Failed expectations.'],

['1/2 You need to be direct and say what you want/need or else people will take advantage of you and ruin everything.',
'2/2 It’s hard to know what to say when you’re invaded by car wash men.'],

['Can an internet Elvis be a decent substitute for a real life Elvis? Things don’t always go as planned and this is disappointing.'],

['1/3 Some objects are seen as more special than others. What makes them special, though?',
'2/3 Things become valuable and get treated differently when they’re called works of art or one-of-a-kind.',
'3/3 But does it matter where your spoon came from?'],
]

hash = '#ELHTO'

#This is where the magic happens
def tweet_fortunes():
    for fortune in sentences:
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
            api.send_direct_message(follower.id, text = 'I\'ve just learned about how to follow people who follow me... Oh, and about DMing. I only send this note once.')

#tweet_fortunes()
#follow_back()
#greet()
