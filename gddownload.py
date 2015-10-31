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


def getFileExtension(filename):
	return filename.split('.')[1]


#Get a list of all files to be uploaded from command line args
def getDownloadList():	
	filelist = []
	numargs = len(sys.argv)
	for i in range (1,numargs):
		filelist.append(sys.argv[i])
	return filelist

#Upload a file to drive with parent folder id = parent_id
def downloadFileFromDrive(service, file_id, file_name):
	if file_id is None:
		appendErrorToLog('File id is null, cannot download.')
		return 
	try:
		request = service.files().get_media(fileId=file_id)
		local_file_name = file_name
		fh = io.FileIO(local_file_name, mode='wb')
		downloader = MediaIoBaseDownload(fh, request, chunksize=1024*1024)

		done = False
		while done is False:
			status, done = downloader.next_chunk()
		if status:
			print "Download %d%%." % int(status.progress() * 100)
		print "Download Complete!"
	

	except errors.HttpError, error:
		appendErrorToLog(error)
	return


drive_service = initializeCredentials()

filelist = getDownloadList()
for fname in filelist:
	fid = getFileId(drive_service, fname)
	downloadFileFromDrive(drive_service, fid, fname)

