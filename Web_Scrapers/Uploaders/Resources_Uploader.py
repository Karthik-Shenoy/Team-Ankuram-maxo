from google.cloud import firestore
from pathlib import Path
import os

#initializing fire base
config = {

	'apiKey': "AIzaSyBxPxs0kQc4aRrBGj7LepvkHZvZ-cYX_Lw",
    'authDomain': "ankuram-maxo-website.firebaseapp.com",
    'databaseURL': "https://ankuram-maxo-website.firebaseio.com",
    'projectId': "ankuram-maxo-website",
    'storageBucket': "ankuram-maxo-website.appspot.com",
    'messagingSenderId': "859628583981",
    'appId': "1:859628583981:web:e2fc9bec965059beb00ca4",
    'measurementId': "G-MM8E3FKJYB"
	
}

#set up environment variables
BASE_DIR = Path(__file__).resolve().parent.parent.parent
KeyFile_Path = str(BASE_DIR)+"\\src\\FireBase_Creds\\KeyFile.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = KeyFile_Path


#inititalizing firestore and database
Fire_Store = firestore.Client()
File = open(str(BASE_DIR)+"\\Web_Scrapers\\Data\\Resources\\Resources_CP_Algorithms.txt", 'r')

num = 168
for line in File:
	#data = {u"Name": user_name, u"Status": '1', u"Uid":uid}
	#Fire_Store.collection(u'user').document(uid).set(data)
	raw = line.split(',')
	n = len(raw[1])
	data = {u"title": raw[0], u"link": raw[1][:n-1], "site": "CP"}
	Fire_Store.collection(u'Resources_Topics').document("Resource-"+str(num)).set(data)
	num+=1