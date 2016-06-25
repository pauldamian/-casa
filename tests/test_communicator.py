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
        pass

    def tearDown(self):
        minimock.restore()

    def testName(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()