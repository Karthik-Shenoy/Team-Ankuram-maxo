from lxml import html, etree
import requests

url = 'https://www.hackerrank.com/domains/algorithms?filters%5Bsubdomains%5D%5B%5D=recursion'
agent = {"User-Agent":'Chrome/70.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
page = requests.get(url, headers=agent)
tree = html.fromstring(page.content)
file = open("E:\\maxo-project\\Team-Ankuram-maxo\\Web_Scrapers\\Data\\Problem_Solving\\Problems_Hacker_Rank.txt", 'a+')


site = "https://www.hackerrank.com/"
problem_titles = tree.xpath('//div[@class="challenge-name-details "]//h4[@class="challengecard-title"]/text()')
problem_difficulty = tree.xpath('//div[@class="challenge-name-details "]//span[contains(@class,"difficulty")]/text()')
problem_links = tree.xpath('//a[@class="js-track-click challenge-list-item"]/@href')


#Topics Done [Searching, Sorting, Dynamic-Programming, Greedy-Algorithms, Bit-Manipulation, Recursion] 

topic = "Recursion"
for i in range(len(problem_titles)):
	line = problem_titles[i]+","+problem_difficulty[i]+","+topic+","+site+problem_links[i]
	file.write(line+"\n")