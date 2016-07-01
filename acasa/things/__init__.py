'''
Created on May 2, 2016

@author: damianpa
'''
THINGS = {'mq2_sensor': {'pin': 18,
                         'type': 'sensor',
                         'location': 'kitchen',
                         'use': 'gas'
                         },
          'dht11_sensor': {'type': 'sensor',
                           'pin': 23,   # BCM, not BOARD numbering
                           'location': 'kitchen',
                           'use': ['temp', 'hum']
                           },
          'ac_dimmer': {'type': 'dimmer',
                        'use': 'lights',
                        'pin': {'sync': 7,
                                'gate': 11
                                },
                        'location': 'undefined'
                        },
          'sensortag': {'type': 'sensor',
                        'use': ['temp', 'hum', 'pressure'],
                        'pin': 'BLE',
                        'location': 'outside',
                        'MAC': 'BC:6A:29:AB:23:E4'}
          }
