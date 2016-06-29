'''
Created on May 2, 2016

@author: damianpa
'''
THINGS = {'mq2_sensor': {'pin': 18,
                         'type': 'mq2',
                         'location': 'kitchen'
                         },
          'dht11_sensor': {'type': 'dht11',
                           'pin': 23,   # BCM, not BOARD numbering
                           'location': 'kitchen'
                           },
          'ac_dimmer': {'type': 'dimmer',
                        'pin': {'sync': 7,
                                'gate': 11
                                },
                        'location': 'undefined'
                        },
          'sensortag': {'type': 'TI Sensortag',
                        'pin': 'BLE',
                        'location': 'outside',
                        'MAC': 'BC:6A:29:AB:23:E4'}
          }
