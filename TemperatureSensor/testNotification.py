#!/usr/bin/python
import time, ConfigParser, os, pycurl, json, MySQLdb, sys
from StringIO import StringIO
#from twilio.rest import TwilioRestClient
import requests

def SendInstaPush(message):
    data_send = {"type": "note", "title": "Temperature Alert", "body": message}
    ACCESS_TOKEN = ""
    resp = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data_send), headers={'Authorization': 'Bearer ' + ACCESS_TOKEN, 'Content-Type': 'application/json'})
SendInstaPush("Hello")
