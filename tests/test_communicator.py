'''
Created on Jun 25, 2016

@author: damianpa
'''
import unittest
import minimock
import sys
sys.path.insert(0, '../acasa/')
import communicator


class Test(unittest.TestCase):

    def setUp(self):
        global message
        message = { 'text': 'show help',
                    'sender': {'screen_name': 'pauldamian8'},
                    'created_at': 'Thu Aug 23 19:45:07 +0000 2017',
                    'id': 23567652346354}

    def tearDown(self):
        minimock.restore()
        communicator.db.delete_command(str(message['id']))

    def testRegiterLatestCommands(self):
        minimock.mock('communicator.Todo.get_latest_id', returns=10)
        minimock.mock('communicator.Twython.get_direct_messages', returns=[message])
        self.assertEqual(communicator.register_latest_commands(), None)
        minimock.mock('communicator.notify', returns="Could not register command. Try again later")
        self.assertEqual(communicator.register_latest_commands(),
                         "Could not register command. Try again later")
        minimock.mock('communicator.Todo.register_command', returns=0)
        minimock.mock('communicator.Twython.get_direct_messages', returns=30 * [message])
        self.assertEqual(communicator.register_latest_commands(), None)
        minimock.mock('communicator.Twython.get_direct_messages', returns=[])
        self.assertEqual(communicator.register_latest_commands(), None)



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()