'''
Created on Jun 25, 2016

@author: damianpa
'''
import unittest
import minimock
import sys
from time import sleep
sys.path.insert(0, '../acasa/lib/')
import reader


class Test(unittest.TestCase):

    def tearDown(self):
        minimock.restore()

    def testInsertReadings(self):
        #minimock.mock('reader.db.insert_reading', returns=0)
        self.assertEqual(reader.register_reading('', 0, 0, 0), None)
        s = ('in', 'out', 'afar%', '@$S$')
        t = (1, 1.2, 0, -12)
        h = (0, 2, 45.67, -33)
        p = (33.33, -900, 90, 0)
        for i in range(4):
            self.assertEqual(reader.register_reading(s[i], t[i], h[i], p[i]), 0)
            sleep(1)
        for i in range(4):
            self.assertEqual(reader.register_reading(p[i], s[i], h[i], s[i]), 1)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testInsertReadings']
    unittest.main()