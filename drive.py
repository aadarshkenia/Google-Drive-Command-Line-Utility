import httplib2
import json
import webbrowser
import logging
import argparse

from oauth2client.client import OAuth2WebServerFlow
from oauth2client import tools
from pprint import pprint
from apiclient.discovery import build
from oauth2client.file import Storage


logging.basicConfig()
with open('client_secret.json') as data_file:    
    data = json.load(data_file)

#Obtain necessary info from client_secret.json
CLIENT_ID = data['installed']['client_id']
CLIENT_SECRET = data['installed']['client_secret']
OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'
REDIRECT_URI = 'http://localhost:8080'

#Generate a url on authorization server
flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE, REDIRECT_URI)


parser = argparse.ArgumentParser(parents=[tools.argparser])
flags = parser.parse_args()

storage = Storage('credentials.dat')
#the get() function returns the credentials for the Storage object. 

credentials = storage.get()
if credentials is None or credentials.invalid:
  credentials = tools.run_flow(flow, storage, flags)
