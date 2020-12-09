from django.shortcuts import render
from pathlib import Path
import os

# Create your views here.
def Problem_Solving_View(request, *args, **kwargs):
	BASE_DIR = Path(__file__).resolve().parent.parent
	loc = os.path.join(BASE_DIR, '\\test\\DB.txt')
	file = open(loc, 'r')
	problems = []
	for line in file:
		curr = line.split(',')
		obj = {}
		print(curr,1)
		obj['name'], obj['difficulty'], obj['topic'], obj['desc'] = curr[0], curr[1], curr[2], curr[3]
		problems.append(obj)
	return render(request, 'Problem_Solving.html',{"problems":problems})

def Login_View(request, *args, **kwargs):
	return render(request, 'loginpage.html',{})

def About_Us_View(request, *args, **kwargs):
	return render(request, 'About_us.html',{})
