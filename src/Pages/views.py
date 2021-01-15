from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib import auth as dj_auth
from pathlib import Path
import uuid
from google.cloud import firestore
import pyrebase
import os
from datetime import datetime
from django.http import HttpResponseRedirect

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

def check_key(dic, item):
	if item in dic:
		return True
	else:
		return False

def Today():
	months = {"01": "Jan", "02": "Feb", "03": "Mar", "04": "Apr", "05": "May", "06": "Jun", "07": "Jul", "08": "Aug", "09": "Sep", "10": "Oct", "11": "Nov", "12": "Dec"}
	now = datetime.now()
	time = str(now).split()[1][:5]
	time_stamp = str(now).split('-')
	ret = months[time_stamp[1]]+" "+time_stamp[2][:2]+", "+time_stamp[0]+"   "+time
	return ret

def ctime(time):
	if(int(time[:2]) > 12):
		ret = str(int(time[:2])-12)+time[2:]+" PM"
	elif(int(time[:2]) == 12 ):
		ret = time+" PM"
	elif(int(time[:2]) == 0):
		ret = str(12)+time[2:]+" AM"
	else:
		ret = time+" AM"
	return ret

def recent_key(item):
	item = item["time_stamp"]
	month = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12}
	print(month[item[:3]], item[4:6], item[8:12], item[14:17], item[18:])
	time = month[item[:3]]*30+int(item[4:6])+int(item[8:12])*365+int(item[14:17])*(1/24)+int(item[18:])*(1/(24*60))
	return time

def trending_key(item):
	return item['comments']

# Create your views here.

def Redirect_Home_View(request, *args, **kwargs):
	return redirect('/home/')

def Problem_Solving_View(request, *args, **kwargs):
	if(not check_key(request.session, 'uid')):
		return redirect("/signin/")
	else:
		user_uid = request.session['uid']
		user = Fire_Store.collection(u'Users').document(user_uid).get().to_dict()
		user_name = user["Name"]

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
				problem["link"] = problem["link"][:-1]
				problems.append(problem)
	elif(valid(topic_list)):
		for doc in problems_ref.stream():
			problem = doc.to_dict()
			if(problem['topic'] in topic_list):
				problem["link"] = problem["link"][:-1]
				problems.append(problem)
	elif(valid(difficulty_list)):
		for doc in problems_ref.stream():
			problem = doc.to_dict()
			if(problem['difficulty'] in difficulty_list):
				problem["link"] = problem["link"][:-1]
				problems.append(problem)
	else:
		for doc in problems_ref.stream():
			problem = doc.to_dict()
			problem["link"] = problem["link"][:-1]
			problems.append(problem)
			


	return render(request, 'Problem_Solving.html',{"problems":problems, "user_name": user_name})

def Signin_View(request, *args, **kwargs):
	return render(request, 'loginpage.html',{})

def Post_Signin_View(request, *args, **kwargs):
	#login_code
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

	if(new_email and new_password):
		try:
			user = auth.create_user_with_email_and_password(new_email, new_password)

			#adding the user into the database
			uid = user['localId']
			data = {u"Name": user_name, u"Status": True, u"Uid":uid}

			Fire_Store.collection(u'Users').document(uid).set(data)
		except Exception as e:
			messages.error(request, "Email already exists", extra_tags = "EMAIL_ALREADY_EXISTS")
			return redirect_signin

	if new_email and (not new_password or not user_name):
		messages.error(request, "Invalid credentials", extra_tags = "INVALID_CREDS_SIGNUP")
		return redirect_signin
	session_id = user['localId']
	request.session['uid'] = str(session_id)
	return redirect_home

def logout(request):
	if(not check_key(request.session, 'uid')):
		return redirect("/signin/")
	else:
		user_uid = request.session['uid']
	dj_auth.logout(request)
	return redirect('/signin/')

def Home_View(request, *args, **kwargs):
	user_name = ""
	if(not check_key(request.session, 'uid')):
		logged_in = 0
	else:
		user_uid = request.session['uid']
		logged_in = 1
		user = Fire_Store.collection(u'Users').document(user_uid).get().to_dict()
		user_name = user["Name"]

	return render(request, 'About_us.html', {"logged_in": logged_in, "user_name": user_name})

def Aptitude_View(request, *args, **kwargs):
	if(not check_key(request.session, 'uid')):
		return redirect("/signin/")
	else:
		user_uid = request.session['uid']
		user = Fire_Store.collection(u'Users').document(user_uid).get().to_dict()
		user_name = user["Name"]

	problems_ref = Fire_Store.collection(u'Aptitude_Problems')
	problems = []

	# topic_list #
	topic_list = []
	for x in range(1,7):
		topic_list.append(request.POST.get("AT"+str(x)))
	print(topic_list, valid(topic_list))


	if(valid(topic_list)):
		for doc in problems_ref.stream():
			problem = doc.to_dict()
			if(problem['topic'] in topic_list):
				problem["link"] = problem["link"][:-1]
				problems.append(problem)
	else:
		for doc in problems_ref.stream():
			problem = doc.to_dict()
			problem["link"] = problem["link"][:-1]
			problems.append(problem)
			
	return render(request, 'Aptitude_Problems_Page.html', {"problems":problems, "user_name": user_name})

def Reset_Page_View(request, *args, **kwargs):
	if(not check_key(request.session, 'uid')):
		return redirect("/signin/")
	else:
		user_uid = request.session['uid']
	resetEmail = request.POST['ResetEmail']
	auth.generate_password_reset_link(resetEmail)
	return render(request, 'resetid.html', {})

def Resources_View(request, *args):
	if(not check_key(request.session, 'uid')):
		return redirect("/signin/")
	else:
		user_uid = request.session['uid']
		user = Fire_Store.collection(u'Users').document(user_uid).get().to_dict()
		user_name = user["Name"]

	resourceSites_ref = Fire_Store.collection(u'Resource_cards')
	siteCards = []
	for doc in resourceSites_ref.stream():
		siteCards.append(doc.to_dict())
	

	return render(request, 'Resources.html', {"siteCards": siteCards, "user_name": user_name})

def Resources_Topic_View(request, val, *args):
	if(not check_key(request.session, 'uid')):
		return redirect("/signin/")
	else:
		user_uid = request.session['uid']
		user = Fire_Store.collection(u'Users').document(user_uid).get().to_dict()
		user_name = user["Name"]
	resourceTopics_ref = Fire_Store.collection(u'Resources_Topics')
	resources = []
	for doc in resourceTopics_ref.stream():
		resource = doc.to_dict()
		if(resource["site"] == str(val)):
			resources.append(resource)
	return render(request, "Resources_Topics.html", {"resources": resources, "user_name": user_name})


def Blog_Page_View(request, *args, **kwargs):
	if(not check_key(request.session, 'uid')):
		return redirect("/signin/")
	else:
		user_uid = request.session['uid']
		user = Fire_Store.collection(u'Users').document(user_uid).get().to_dict()
		user_name = user["Name"]

	Blog_Posts = Fire_Store.collection(u'Blog-Posts')
	previews = []
	trending_posts = []
	for post in Blog_Posts.stream():
		Blog_Post = post.to_dict()
		date = Blog_Post["time_stamp"][:13]
		time = ctime(Blog_Post["time_stamp"].split()[3])
		preview = {"title": Blog_Post["title"], "p_text": Blog_Post["body"][:300], "time_stamp": Blog_Post["time_stamp"], "User_Name": Blog_Post["User_Name"], "Blog_id": Blog_Post["Blog_id"], "date": date, "time": time, "comments": Blog_Post["comments"]}
		previews.append(preview)
		trending_posts.append(Blog_Post)

	previews.sort(key=recent_key, reverse=True)
	trending_posts.sort(key=trending_key, reverse=True)
	trending_posts = trending_posts[:5]

	return render(request, "Blog-New.html", {"recent_posts": previews, "trending_posts": trending_posts, "user_name": user_name})

def Blog_Page_Sort_View(request, topic, *args, **kwargs):
	if(not check_key(request.session, 'uid')):
		return redirect("/signin/")
	else:
		user_uid = request.session['uid']
		user = Fire_Store.collection(u'Users').document(user_uid).get().to_dict()
		user_name = user["Name"]

	Blog_Posts = Fire_Store.collection(u'Blog-Posts')
	previews = []
	trending_posts = []
	for post in Blog_Posts.stream():
		Blog_Post = post.to_dict()
		if(Blog_Post["topic"]==topic):
			date = Blog_Post["time_stamp"][:13]
			time = ctime(Blog_Post["time_stamp"].split()[3])
			preview = {"title": Blog_Post["title"], "p_text": Blog_Post["body"][:300], "time_stamp": Blog_Post["time_stamp"], "User_Name": Blog_Post["User_Name"], "Blog_id": Blog_Post["Blog_id"], "date": date, "time": time, "comments": Blog_Post["comments"]}
			previews.append(preview)
		trending_posts.append(Blog_Post)

	previews.sort(key=recent_key, reverse=True)
	trending_posts.sort(key=trending_key, reverse=True)
	trending_posts = trending_posts[:5]

	return render(request, "Blog-New.html", {"recent_posts": previews, "trending_posts": trending_posts})


def Blog_Single_View(request, blog_id, *args, **kwargs):
	if(not check_key(request.session, 'uid')):
		return redirect("/non-user/")
	else:
		user_uid = request.session['uid']
		user = Fire_Store.collection(u'Users').document(user_uid).get().to_dict()
		user_name = user["Name"]
	# access the respective blog using its id #
	curr_post = Fire_Store.collection(u'Blog-Posts').document(blog_id).get()
	curr_post = curr_post.to_dict()
	# /////////////////////////////////////// #

	# Comments Post Section #
	user_uid = request.session['uid'] 
	user = Fire_Store.collection(u'Users').document(user_uid).get()
	user = user.to_dict()
	comment = request.POST.get("message")
	user_name = user["Name"]
	time_stamp = Today()
	if(comment):
		gen_id = uuid.uuid1()
		date = time_stamp[:13]
		time = ctime(time_stamp.split()[3])
		Comment_Post = {"User_Name": user_name, "Uid": user_uid, "time": time, "data": comment, "Blog_id": blog_id, "date": date, "time_stamp": time_stamp}
		Fire_Store.collection(u'Comments').document(str(gen_id.hex)).set(Comment_Post)
		curr_post["comments"]+=1
		Fire_Store.collection(u'Blog-Posts').document(blog_id).set(curr_post)
		return HttpResponseRedirect("/blog-single/"+blog_id)
	else:
		messages.error(request, "Enter the required fields", extra_tags = "INVALID_COMMENT_DATA")
	# // Comments Post Section #
	
	# Comment display section #
	Comments = Fire_Store.collection(u'Comments')
	disp_comms = []
	for comm in Comments.stream():
		curr_comment = comm.to_dict()
		if(curr_comment["Blog_id"] == blog_id):
			disp_comms.append(curr_comment)
	# // Comment display section #
	disp_comms.sort(key=recent_key, reverse=True)
	
	return render(request, "blog-single.html", {"current_post": curr_post, "current_comments": disp_comms, "user_name":user_name})


def Manage_Posts_View(request, *args, **kwargs):
	if(not check_key(request.session, 'uid')):
		return redirect("/non-user/")
	else:
		user_uid = request.session['uid']
		user = Fire_Store.collection(u'Users').document(user_uid).get().to_dict()
		user_name = user["Name"]

	user_uid = request.session['uid'] 
	Blog_Posts = Fire_Store.collection(u'Blog-Posts')
	users_posts = []
	for post in Blog_Posts.stream():
		Blog_Post = post.to_dict()
		if(user_uid == Blog_Post["Uid"]):
			users_posts.append(Blog_Post)	
	return render(request, "Manage-Posts.html", {"Posts": users_posts, "user_name": user_name})

def Edit_Post_View(request, blog_id, *args, **kwargs):
	if(not check_key(request.session, 'uid')):
		return redirect("/non-user/")
	else:
		user_uid = request.session['uid']
		user = Fire_Store.collection(u'Users').document(user_uid).get().to_dict()
		user_name = user["Name"]
	# access the respective blog using its id #
	curr_post = Fire_Store.collection(u'Blog-Posts').document(blog_id).get()
	curr_post = curr_post.to_dict()
	# /////////////////////////////////////// #
	edited_title = request.POST.get("title")
	edited_body = request.POST.get("body")
	edited_topic = request.POST.get("topic")
	print(edited_topic, edited_body)
	if edited_body and edited_title:
		curr_post["body"] = edited_body
		curr_post["title"] = edited_title
		curr_post["topic"] = edited_topic
		Fire_Store.collection(u'Blog-Posts').document(blog_id).set(curr_post)
		return HttpResponseRedirect("/manage-posts/")
	else:
		messages.error(request, "Enter the required fields", extra_tags = "INVALID_BLOG_DATA")
	 

	return render(request, "Edit-Post.html", {"current_post": curr_post, "user_name":user_name})

def Delete_Post(request, blog_id, *args, **kwargs):
	if(not check_key(request.session, 'uid')):
		return redirect("/non-user/")
	else:
		user_uid = request.session['uid']
	Fire_Store.collection(u'Blog-Posts').document(blog_id).delete()
	return redirect("/manage-posts/")

def Create_Post_View(request, *args, **kwargs):
	if(not check_key(request.session, 'uid')):
		return redirect("/non-user/")
	else:
		user_uid = request.session['uid']
		user = Fire_Store.collection(u'Users').document(user_uid).get().to_dict()
		user_name = user["Name"]

	title = request.POST.get("title")
	body = request.POST.get("body")
	topic = request.POST.get("topic")

	# getting the user #
	user_uid = request.session['uid'] 
	user = Fire_Store.collection(u'Users').document(user_uid).get()
	user = user.to_dict()
	user_name = user['Name']
	# // getting the user #
	time_stamp = Today()

	# Posting the Blog #
	if body and title:
		gen_id = uuid.uuid1()
		date = time_stamp[:13]
		time = ctime(time_stamp.split()[3])
		Blog_Post = {"title": str(title), "body": str(body), "time_stamp": str(time_stamp), "User_Name":user_name, "Uid": user_uid, "Blog_id": str(gen_id.hex), "comments": 0, "date": date, "time": time, "topic": topic}
		Fire_Store.collection(u'Blog-Posts').document(str(gen_id.hex)).set(Blog_Post)
		return HttpResponseRedirect("/create-post/")
	else:
		messages.error(request, "Enter the required fields", extra_tags = "INVALID_BLOG_DATA")
	# // Posting the Blog #

	return render(request, "Create-Post.html", {"user_name":user_name})
