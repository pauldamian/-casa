'''
Created on 4 apr. 2016

@author: Paul
'''
import requests

def get_response(request_url):
    return requests.get(request_url).json()