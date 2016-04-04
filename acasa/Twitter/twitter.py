'''
Created on Mar 19, 2016

@author: damianpa
'''
from twython import Twython
from twython.exceptions import TwythonError
from datetime import datetime
from time import sleep

from Utils import log
from Utils import resources as r

tweet = Twython(r.C_KEY, r.C_SECRET, r.A_TOKEN, r.A_SECRET)
valid_commands = ['execute', 'help'] # turn to sets

executed_commands = []

class Command:

    def create_command(self, cid, message, data, commander):
        if message.lower() not in valid_commands:
            log.write("%s is not a valid command. Skipping command initialization." % message)
            return None
        elif cid in executed_commands:
            log.write("Command was executed already")
            return None
        else:
            self.message = message.lower()
            self.cid = cid
            self.date = data
            self.commander = commander
            return self

    def send_help(self):
        text = "The current set of available commands includes:\n \
        Help - displays this message\n \
        Execute - does nothing"
        notify(text, self.commander)

    def execute(self):
        pass

    commands = {'execute': execute, 'help': send_help}

    def execute_command(self):
        executed_commands.append(self.cid)
        self.commands[self.message](self)


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


def latest_messages(messages):
    recent_messages = []
    month_dict = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
                  "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
    ten_mins_back = datetime.now() - datetime.timedelta(minutes=122)

    for message in messages:
        data = message['created_at'] # Sun Mar 20 11:47:28 +0000 2016 strftime
        parts = data.split(" ")
        hour = parts[3].split(":")
        m_date = datetime(int(parts[5]), month_dict[parts[1]], int(parts[2]),
                          int(hour[0]), int(hour[1]), int(hour[2]))
        if ten_mins_back < m_date:
            recent_messages.append(message)
    return recent_messages


def execute_latest_commands():
    messages = tweet.get_direct_messages()
    new_messages = latest_messages(messages)
    commands = []
    for message in new_messages:
        try:
            comanda = Command()
            command = comanda.create_command(message['id'], message['text'].strip(), message['created_at'], message['sender']['screen_name'])
            if command is not None:
                commands.append(command)
        except UnicodeEncodeError:
            log.write("Cannot decode message with id = " + str(message['id']))
    for command in commands:
        command.execute_command()
        sleep(5)

while True:
    execute_latest_commands()
    sleep(60)
