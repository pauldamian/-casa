import datetime
from time import sleep
from twython import Twython
from twython.exceptions import TwythonError

from lib import util
from lib.todo import Todo
from lib import constants
from lib import command

K = util.get_conf_value(constants.KEY_TWITTER)

tweet = Twython(K['C_KEY'], K['C_SECRET'], K['A_TOKEN'], K['A_SECRET'])
seen_messages = []
db = Todo()
mid = 0 # max id per twitter


# def send_help(commander):
#     text = "The current set of commands includes:\n\
#     Show temp | hum | forecast | weather | commands - returns sensor readings\n\
#     Lights off | <intensity> | on - controls the lightning\n\
#     Cancel <command_name> - cancels next command of type <command_name>\n\
#     Help [command] - displays this message or specific command help"
#     notify(text, commander)


def notify(message, username):
    '''
    Notifies the user by sending a direct message on Twitter
    Parameters:
        message: notification text (string)
        username: the twitter name of the user to notify (string)
    '''
    try:
        status = tweet.send_direct_message(user=username, text=message)
        util.log("Successfully sent message with id = " + str(status['id']))
        return status['id']
    except TwythonError as te:
        util.log("Could not send message due to Twython Error: " + te.msg)
    return 0


def register_latest_commands():
    global mid
    lid = max(db.get_latest_id(), mid) # max id / registered commands
    if(lid > 0):
        try:
            new_messages = tweet.get_direct_messages(since_id=lid)
        except TwythonError as te:
            util.log(te.message)
            return
        status = constants.STATUS_NEW
    else:
        new_messages = tweet.get_direct_messages(count=1)
        status = constants.STATUS_NOTIFIED
    for message in new_messages:
        username = message['sender']['screen_name']
        text = message['text'].strip().lower()
        if text.split()[0] == 'help':
            text = 'show ' + text
        data = datetime.datetime.strptime(message['created_at'], '%a %b %d %H:%M:%S +%f %Y')
        mid = max(message['id'], mid)
        try:
            cmd = command.Command(text, username, status=status, cid=mid, date=str(data))
        except ValueError, ve:
            notify(ve, username)
        db.insert_command(cmd)


def respond():
    results = db.get_completed_commands()
    for res in results:
        notify(res.result, res.commander)
        db.update_command_status(res.cid, constants.STATUS_NOTIFIED)


def run():
    util.log('Twitter process started')
    i = 1
    while True:
        # responds every 3 seconds
        respond()
        sleep(3)
        i += 1
        if i == 10:
            # takes new commands every 30 seconds
            register_latest_commands()
            i = 1
