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
from laverdadb import get_db_instance
from command import Command

tweet = Twython(r.C_KEY, r.C_SECRET, r.A_TOKEN, r.A_SECRET)
seen_messages = []
db = get_db_instance()


def send_help(commander):
    text = "The current set of commands includes:\n\
    Show - returns sensor readings\n\
    Lights - controls the lightning\n\
    Help - displays this message"
    notify(text, commander)


def register_command(cid, message, data, commander, status='NEW'):
    com = Command(cid, message, data, commander, status)
    if(com.cid == 0):
        log.write("%s is not a valid command. Check the set of valid commands" % message)
        send_help(commander)
    else:
        db.insert_command(com)


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


##def latest_messages(messages):
##    recent_messages = []
##    month_dict = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
##                  "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
##    ten_mins_back = datetime.datetime.now() - datetime.timedelta(minutes=190)
##
##    for message in messages:
##        data = message['created_at'] # Sun Mar 20 11:47:28 +0000 2016 strftime
##        parts = data.split(" ")
##        hour = parts[3].split(":")
##        m_date = datetime.datetime(int(parts[5]), month_dict[parts[1]], int(parts[2]),
##                                   int(hour[0]), int(hour[1]), int(hour[2]))
##        if ten_mins_back < m_date:
##            recent_messages.append(message)
##    return recent_messages


def register_latest_commands():
    lid = db.get_latest_id()
    if(lid > 0):
        new_messages = tweet.get_direct_messages(since_id=lid)
        status = 'NEW'
    else:
        new_messages = tweet.get_direct_messages(count=1)
        status = 'COMPLETED'
    for message in new_messages:
        data = datetime.datetime.strptime(message['created_at'], '%a %b %d %H:%M:%S +%f %Y')
        register_command(message['id'], message['text'].strip(), str(data), message['sender']['screen_name'], status)


def run():
    while True:
        register_latest_commands()
        sleep(61)
