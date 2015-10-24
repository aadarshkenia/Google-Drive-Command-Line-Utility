import httplib2
import json
import webbrowser
import logging
import argparse

from oauth2client.client import OAuth2WebServerFlow
from oauth2client import tools
from oauth2client.file import Storage
from pprint import pprint
from apiclient.discovery import build
from apiclient import errors
from apiclient.http import MediaFileUpload

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
	storage.put(credentials)

#Use the authorize() function of the Credentials class to apply necessary credential headers to all requests made by an httplib2.Http instance
http = httplib2.Http()
http = credentials.authorize(http)

drive_service = build('drive', 'v2', http=http)

#Retrieve a parent folder's id given folder name and mime type in query
parent_id = None
result = []
try:
	search_query ="title = 'CMD Test' and mimeType = 'application/vnd.google-apps.folder'	"
	files = drive_service.files().list(q=search_query).execute()
	result.extend(files['items'])
	for f in result:
		parent_id = f['id']
except errors.HttpError, error:
	print 'An error occurred: %s' % error

'''
#Retrieve file metadata using file id
try:
	if file_id is not None:
		myfile = drive_service.files().get(fileId=file_id).execute()
		print 'Title: %s' % myfile['title']
		print 'MIME type: %s' %myfile['mimeType']
	else:
		print 'File id is null.'
except errors.HttpError, error:
	print 'An error occurred: %s' % error

'''
filename = 'Test1.pdf'
mime_type = 'application/pdf'
title = 'Test1-Changed title'
description = 'First test file upload'

#Insert a file into folder
media_body = MediaFileUpload(filename, mimetype=mime_type, resumable=True)
body = {'title': title,'description': description,'mimeType': mime_type}

# Set the parent folder.
if parent_id:
    body['parents'] = [{'id': parent_id}]

try:
    file = drive_service.files().insert(
        body=body,
        media_body=media_body).execute()
except errors.HttpError, error:
    print 'An error occured: %s' % error
    



