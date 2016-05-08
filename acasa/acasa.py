'''
Created on 20 apr. 2016

@author: Paul
'''
from __init__ import set_test_mode
set_test_mode()
import log
import twitter
import executor

import multiprocessing

if __name__ == "__main__":
    processes = []
    for func in [executor.run, twitter.test_run]:
        processes.append(multiprocessing.Process(target=func))
        processes[-1].start()
        log.write("Process %s started" % func.__name__)
