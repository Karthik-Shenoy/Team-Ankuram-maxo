from lxml import html, etree
import requests
from selenium import webdriver

def reduce(s):
	size = 0
	for i in range(len(s)-1):
		if(s[i] == " " and s[i+1] == "-" ):
			break
		size+=1
	return s[:size]

def conv_perc(s):
	size = 0
	for i in range(len(s)):
		if(s[i] == "%"):
			break
		size+=1
	return s[:size]

url = 'https://www.codechef.com/tags/problems/implementation'
file = open("E:\\maxo-project\\Team-Ankuram-maxo\\Web_Scrapers\\Data\\Problem_Solving\\Problems_Code_Chef.txt", 'a+')
driver = webdriver.PhantomJS()
driver.get(url)

problem_titles = driver.find_elements_by_xpath('//div[@class="problem-tagbox-inner"]/div[1]/a')
problem_difficulty = driver.find_elements_by_xpath('//div[@class="problem-tagbox-head-inner"]/div[2]/span')

#Topics Done ["Time-Complexity"]
topic = "Time-Complexity"
site = "https://www.codechef.com"
for i in range(20):
	title = reduce(problem_titles[i].text)
	perc = conv_perc(problem_difficulty[i].text)
	link = problem_titles[i].get_attribute("href")
	if(float(perc) > 60):
		diff = "Easy"
	elif(float(perc) > 30):
		diff = "Medium"
	else:
		diff = "Hard"
	print(title, diff, link)
	line = title+","+diff+","+topic+","+link
	file.write(line+"\n")
