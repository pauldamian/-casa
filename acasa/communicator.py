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
from todo import Todo

tweet = Twython(r.C_KEY, r.C_SECRET, r.A_TOKEN, r.A_SECRET)
seen_messages = []
db = Todo()
mid = 0 # max id per twitter


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
    global mid
    lid = max(db.get_latest_id(), mid) # max id / registered commands
    if(lid > 0):
        try:
            new_messages = tweet.get_direct_messages(since_id=lid)
        except TwythonError as te:
            log.write(te.message)
            return
        status = 'NEW'
    else:
        new_messages = tweet.get_direct_messages(count=1)
        status = 'COMPLETED'
    for message in new_messages:
        # Take commands only from authorized users
        # These users must be stored in a list called USERS in the resources file
        # print message['sender']['location']
        username = message['sender']['screen_name']
        data = datetime.datetime.strptime(message['created_at'], '%a %b %d %H:%M:%S +%f %Y')
        mid = max(message['id'], mid)
        res = db.register_command(mid, message['text'].strip(), str(data), username, status)
        if res != 0:
            notify('Could not register command. Try again later', username)


def respond():
    results = db.get_completed_commands()
    for res in results:
        notify(res.result, res.commander)
        db.update_command_status(res.cid, 'NOTIFIED')


def run():
    log.write('Twitter process started')
    i = 1
    while True:
        respond()
        sleep(3)
        i += 1
        if i == 20:
            register_latest_commands()
            i = 1


def test_run():
    while True:
        lid = db.get_latest_id()
        message = raw_input('Your wish is my command: ')
        status = 'NEW'
        data = datetime.datetime.now()
        db.register_command(lid + 1, message, data, 'pauldamian8', status)
