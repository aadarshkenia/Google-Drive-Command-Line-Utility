import httplib2
import json
import webbrowser
import logging
import argparse
import sys
import time
import datetime

from oauth2client.client import OAuth2WebServerFlow
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.discovery import build
from apiclient import errors
from apiclient.http import MediaFileUpload

root_path = '/home/aadarsh-ubuntu/Desktop/Summer Projs/CMDUtility/'
#Obtains auth token and initializes service object for making API calls
def initializeCredentials():
	logging.basicConfig()
	with open(root_path+'client_secret.json') as data_file:    
		data = json.load(data_file)

	#Obtain necessary info from client_secret.json
	CLIENT_ID = data['installed']['client_id']
	CLIENT_SECRET = data['installed']['client_secret']
	OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'
	REDIRECT_URI = 'http://localhost:8080'

	#Generate a url on authorization server
	flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE, REDIRECT_URI)

	storage = Storage(root_path+'credentials.dat')
	#the get() function returns the credentials for the Storage object. 

	credentials = storage.get()
	if credentials is None or credentials.invalid:
		credentials = tools.run_flow(flow, storage, flags)
		storage.put(credentials)

	#Use the authorize() function of the Credentials class to apply necessary credential headers to all requests made by an httplib2.Http instance
	http = httplib2.Http()
	http = credentials.authorize(http)

	#Google service object used to make API calls
	drive_service = build('drive', 'v2', http=http)
	return drive_service

def appendErrorToLog(message):
	#Do something about the exception
	fo = open(root_path+'logfile.txt', "a")
	curr_time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
	fo.write("ERROR:\t"+curr_time+"\n"+"%s\n\n\n\n" %message)
	fo.close()

def getParentFolderId(foldername):
	result = []
	parent_id = None
	try:
		search_query ="title = '"+foldername+"' and mimeType = 'application/vnd.google-apps.folder'"
		files = drive_service.files().list(q=search_query).execute()
		result.extend(files['items'])
		for f in result:
			parent_id = f['id']
	except errors.HttpError, error:
		appendErrorToLog(error)
	return parent_id


#Get a list of all files to be uploaded from command line args
def getUploadList():	
	filelist = []
	numargs = len(sys.argv)
	for i in range (1,numargs):
		filelist.append(sys.argv[i])
	return filelist

#Upload a file to drive with parent folder id = parent_id
def uploadFileToDrive(service, filename, parent_id):
	title = filename
	#Insert a file into folder
	media_body = MediaFileUpload(filename, resumable=True)
	body = {'title': title}
	# Set the parent folder.
	if parent_id:
	    body['parents'] = [{'id': parent_id}]
	else:
		err_msg = "Could not find parent folder."
		appendErrorToLog(err_msg)
	try:
	    file = drive_service.files().insert(body=body, media_body=media_body).execute()
	except errors.HttpError, error:
	    appendErrorToLog(error)
	return


drive_service = initializeCredentials()
#Folder name be passed here: maybe 1st command line arg?
foldername='CMD Test' #for now static
parent_id=getParentFolderId(foldername)

#Retrieve each file from command line args and upload to drive
fileUploadList = getUploadList()
for f in fileUploadList:
	uploadFileToDrive(drive_service, f, parent_id)

