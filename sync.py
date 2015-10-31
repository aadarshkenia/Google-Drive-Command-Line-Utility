import httplib2
import json
import webbrowser
import logging
import argparse
import sys
import time
import datetime
import io

from oauth2client.client import OAuth2WebServerFlow
from oauth2client import tools
from oauth2client.file import Storage
from apiclient.discovery import build
from apiclient import errors
from apiclient.http import MediaFileUpload
from apiclient.http import MediaIoBaseDownload
from StringIO import StringIO

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

#Get file/folder id to be downloaded
def getFileId(service, fname):
	result = []
	file_id = None
	try:
		search_query ="title = '"+fname+"'"
		files = service.files().list(q=search_query).execute()
		result.extend(files['items'])
		for f in result:
			file_id = f['id']
			#print file_id
	except errors.HttpError, error:
		appendErrorToLog(error)
		return None
	return file_id

#Get file/folder name from id
def getFilenameFromId(service, file_id):
	file = service.files().get(fileId=file_id).execute()
	return file['title']


#Get all files and subfolders with this folder as parent folder
def getFilesInFolder(service, foldername):
	folder_id = getFileId(service, foldername)
	children_list = []
	page_token = None
	try:
		param = {}
		
		param['pageToken'] = page_token
		search_query = "folderId='"+folder_id+"'"
		children = service.children().list(folderId=folder_id).execute()
		for child in children.get('items', []):
			print 'File Name: %s' %getFilenameFromId(service, child['id'])
		page_token = children.get('nextPageToken')
			
	except errors.HttpError, error:
		appendErrorToLog(error)
	return


drive_service = initializeCredentials()
#The foldername to be synced will be passed as a command line argument
foldername = sys.argv[1]
#children_list = getFilesInFolder(drive_service, foldername, parent_folder_id)
getFilesInFolder(drive_service, foldername)