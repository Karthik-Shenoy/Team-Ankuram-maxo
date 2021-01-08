from django.shortcuts import render, redirect
from django.contrib import messages
from pathlib import Path
from google.cloud import firestore
import pyrebase
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
BASE_DIR = Path(__file__).resolve().parent.parent
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(BASE_DIR, "FireBase_Creds\\KeyFile.json")


#inititalizing firestore and database
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
dataBase = firebase.database()
Fire_Store = firestore.Client()

def valid(lst):
	for x in lst:
		if(x):
			return True
	return False

# Create your views here.
def Problem_Solving_View(request, *args, **kwargs):
	problems_ref = Fire_Store.collection(u'Problems')
	problems = []

	# difficulty_list #
	difficulty_list = []
	for x in range(1,4):
		difficulty_list.append(request.POST.get("D"+str(x)))
	# topic_list #
	topic_list = []
	for x in range(1,11):
		topic_list.append(request.POST.get("T"+str(x)))
	print(topic_list, valid(topic_list))
	print(difficulty_list, valid(difficulty_list))


	if(valid(topic_list) and valid(difficulty_list)):
		for doc in problems_ref.stream():
			problem = doc.to_dict()
			if(problem['topic'] in topic_list and problem['difficulty'] in difficulty_list):
				problems.append(problem)
	elif(valid(topic_list)):
		for doc in problems_ref.stream():
			problem = doc.to_dict()
			if(problem['topic'] in topic_list):
				problems.append(problem)
	elif(valid(difficulty_list)):
		for doc in problems_ref.stream():
			problem = doc.to_dict()
			if(problem['difficulty'] in difficulty_list):
				problems.append(problem)
	else:
		for doc in problems_ref.stream():
			problems.append(doc.to_dict())
			


	return render(request, 'Problem_Solving.html',{"problems":problems})

def Signin_View(request, *args, **kwargs):
	return render(request, 'loginpage.html',{})

def Post_Signin_View(request, *args, **kwargs):
	#login_code
	print(1)
	email = request.POST.get('signInEmail')
	password = request.POST.get('signInPassword')
	redirect_signin = redirect('/signin/')
	redirect_home = redirect('/home/')
	if(email and password):
		try:
			user = auth.sign_in_with_email_and_password(email, password)
		except Exception as e:			
			messages.error(request, "Invalid credentials", extra_tags = "INVALID_CREDS_SIGNIN")
			return redirect_signin

	if email and not password:
		messages.error(request, "Invalid credentials", extra_tags = "INVALID_CREDS_SIGNIN")
		return redirect_signin

	#sign_up_code
	user_name = request.POST.get('userName')
	new_email = request.POST.get('signUpEmail')
	new_password = request.POST.get('signUpPassWord')

	print(new_email, new_password)
	if(new_email and new_password):
		try:
			user = auth.create_user_with_email_and_password(new_email, new_password)

			#adding the user into the database
			uid = user['localId']
			data = {u"Name": user_name, u"Status": '1', u"Uid":uid}

			Fire_Store.collection(u'user').document(uid).set(data)
		except Exception as e:
			messages.error(request, "Email already exists", extra_tags = "EMAIL_ALREADY_EXISTS")
			return redirect_signin

	if new_email and (not new_password or not user_name):
		messages.error(request, "Invalid credentials", extra_tags = "INVALID_CREDS_SIGNUP")
		return redirect_signin

	return redirect_home

def About_Us_View(request, *args, **kwargs):
	return render(request, 'About_us.html', {})

def Aptitude_View(request, *args, **kwargs):
	problems_ref = Fire_Store.collection(u'Problems')
	problems = []

	# topic_list #
	topic_list = []
	for x in range(1,6):
		topic_list.append(request.POST.get("AT"+str(x)))
	print(topic_list, valid(topic_list))


	if(valid(topic_list)):
		for doc in problems_ref.stream():
			problem = doc.to_dict()
			if(problem['topic'] in topic_list):
				problems.append(problem)
	else:
		for doc in problems_ref.stream():
			problems.append(doc.to_dict())
			
	return render(request, 'Aptitude_Problems_Page.html', {"problems":problems})

def Home_View(request, *args, **kwargs):
	return render(request, 'home.html', {})

def Reset_Page_View(request, *args, **kwargs):
	resetEmail = request.POST['ResetEmail']
	auth.generate_password_reset_link(resetEmail)
	return render(request, 'resetid.html', {})

def Resources_View(request, *args):
	resourceSites_ref = Fire_Store.collection(u'Resource_cards')
	siteCards = []
	for doc in resourceSites_ref.stream():
		siteCards.append(doc.to_dict())

	resourceTopics_ref = Fire_Store.collection(u'Resources_Topics')
	resources = []
	for doc in resourceTopics_ref.stream():
		resource = doc.to_dict()
		resources.append(resource)
	print(resources)

	if request.POST.get("GFG"):
		return render(request, 'Resources_Topics.html', {"resources": resources, "val": "GFG"})
	
	elif request.POST.get("TP"):
		return render(request, 'Resources_Topics.html', {"resources": resources, "val": "TP"})
	
	elif request.POST.get("CP"):
		return render(request, 'Resources_Topics.html', {"resources": resources, "val": "CP"})
	
	elif request.POST.get("W3"):
		return render(request, 'Resources_Topics.html', {"resources": resources, "val": "W3"})
	
	elif request.POST.get("CF"):
		return render(request, 'Resources_Topics.html', {"resources": resources, "val": "CF"})

	return render(request, 'Resources.html', {"siteCards": siteCards})


def ChatBot(request, *args, **kwargs):
	return render(request, "Chatbot.html", {})

def Post_Chat(request, *args, **kwargs):
	msg = request.POST.get('userMsg')
	print(msg)
	redirect_chat = redirect('/chatbot/')
	return redirect_chat