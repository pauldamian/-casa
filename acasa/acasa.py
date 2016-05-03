'''
Created on 20 apr. 2016

@author: Paul
'''
import log
import twitter
import executor

import time
import multiprocessing

if __name__ == "__main__":
    processes = []
    for func in [twitter.run, executor.run]:
        processes.append(multiprocessing.Process(target=func))
        processes[-1].start()
        log.write("Process %s started" % func.__name__)

    # Do stuff

    while True:
        time.sleep(600) # sleep for 10 minutes
        living_processes = [p.is_alive() for p in processes]
        if living_processes < 3:
            for p in living_processes:
                p.terminate()
            print("Oops: Some processes died")
        # do other error handling here if necessary
