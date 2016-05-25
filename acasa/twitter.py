'''
Created on Mar 19, 2016

@author: damianpa
'''
from twython import Twython
from twython.exceptions import TwythonError
import datetime
from time import sleep

import log
import resources as r
from laverdadb import Laverdadb
from command import Command

tweet = Twython(r.C_KEY, r.C_SECRET, r.A_TOKEN, r.A_SECRET)
seen_messages = []
db = Laverdadb()


def send_help(commander):
    text = "The current set of commands includes:\n\
    Show - returns sensor readings\n\
    Lights - controls the lightning\n\
    Help - displays this message"
    notify(text, commander)


def notify(message, username):
    '''
    Notifies the user by sending a direct message on Twitter
    Parameters:
        message: notification text (string)
        username: the twitter name of the user to notify (string)
    '''
    try:
        status = tweet.send_direct_message(user=username, text=message)
        log.write("Successfully sent message with id = " + str(status['id']))
        return status['id']
    except TwythonError as te:
        log.write("Could not send message due to Twython Error: " + te.msg)
    return 0


def register_latest_commands():
    lid = db.get_latest_id()
    if(lid > 0):
        new_messages = tweet.get_direct_messages(since_id=lid)
        status = 'NEW'
    else:
        new_messages = tweet.get_direct_messages(count=1)
        status = 'COMPLETED'
    for message in new_messages:
        # Take commands only from authorized users
        # These users must be stored in a list called USERS in the resources file
        username = message['sender']['screen_name']
        data = datetime.datetime.strptime(message['created_at'], '%a %b %d %H:%M:%S +%f %Y')
        res = db.register_command(message['id'], message['text'].strip(), str(data), username, status)
        if res != 0: 
            notify('Could not register command. Try again later', username)


def run():
    while True:
        register_latest_commands()
        sleep(61)


def test_run():
    while True:
        lid = db.get_latest_id()
        message = raw_input('Your wish is my command: ')
        status = 'NEW'
        data = datetime.datetime.now()
        db.register_command(lid + 1, message, data, 'pauldamian8', status)
