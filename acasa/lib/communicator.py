import sys
import datetime
from time import sleep
import twython

from lib import util, log
from lib.db_connector import DBConnector
from lib import constants
from lib import command

# avoid log pollution
log.getLogger("oauthlib").setLevel(log.INFO)
log.getLogger("requests_oauthlib").setLevel(log.INFO)

tweet = None
seen_messages = []
db = None
mid = 0  # max message id from twitter


# def send_help(commander):
#     text = "The current set of commands includes:\n\
#     Show temp | hum | forecast | weather | commands - returns sensor readings\n\
#     Lights off | <intensity> | on - controls the lightning\n\
#     Cancel <command_name> - cancels next command of type <command_name>\n\
#     Help [command] - displays this message or specific command help"
#     notify(text, commander)


def notify(message, username):
    """
    Notifies the user by sending a direct message on Twitter
    Parameters:
        message: notification text (string)
        username: the twitter name of the user to notify (string)
    """
    try:
        log.info("Sending message {} to {}".format(message, username))
        status = tweet.send_direct_message(user=username, text=message)
        log.info("Successfully sent message with id = " + str(status['id']))
        return status['id']
    except (twython.TwythonAuthError, twython.TwythonError) as te:
        log.error("Could not send message due to Twython Error: " + te.msg)


def register_latest_commands():
    global mid
    # TODO find a way to get only "unread" messages
    lid = max(db.get_greatest_property("msg_id", 0), mid)  # max id / registered commands
    if lid > 0:
        try:
            new_messages = tweet.get_direct_messages(since_id=lid)
        except twython.TwythonError as te:
            log.info("Unable to get direct messages since id {}: {}".format(lid, te))
            return
        status = constants.STATUS_NEW
    else:
        try:
            new_messages = tweet.get_direct_messages(count=1)
        except twython.TwythonError as te:
            log.info("Unable to get latest direct message: {}".format(te))
            return
        status = constants.STATUS_NOTIFIED

    for message in new_messages[:3]:
        username = message['sender']['screen_name']
        text = message['text'].strip().lower()
        if text.split()[0] == 'help':
            text = 'show ' + text

        data = datetime.datetime.strptime(message['created_at'], '%a %b %d %H:%M:%S +%f %Y')
        mid = message.get("id")
        try:
            cmd = command.Command(text, username, status=status, date=str(data), msg_id=mid)
            db.insert_command(cmd)
        except (ValueError, AttributeError) as ve:
            log.error(ve)
            notify(ve, username)


def respond():
    results = db.get_completed_commands()
    for res in results:
        try:
            notify(res.result, res.user)
            db.update_command(res.cmd_id, "status", constants.STATUS_NOTIFIED)
        except AttributeError as ae:
            log.error(ae)
            db.update_command(res.cmd_id, "status", constants.STATUS_NOT_NOTIFIED)


def run():
    log.info('Communicator process started')
    global tweet, db
    try:
        k = util.get_conf_value(constants.KEY_TWITTER)
        tweet = twython.Twython(k['C_KEY'], k['C_SECRET'], k['A_TOKEN'], k['A_SECRET'])
    except KeyError as ke:
        log.error(ke)
        sys.exit(1)

    db = DBConnector()

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


if __name__ == "__main__":
    run()
