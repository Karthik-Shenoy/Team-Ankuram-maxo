from lxml import html, etree
import requests
​
​
url = 'https://cp-algorithms.com/'
agent = {"User-Agent":'Chrome/71.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
page = requests.get(url, headers=agent)
tree = html.fromstring(page.content)
file = open("E:\\maxo-project\\Team-Ankuram-maxo\\Web_Scrapers\\Data\\Resources\\Resources_CP_Algorithms.txt", 'a+')
​
resource_titles = tree.xpath('//li/a/text()')
resource_links = tree.xpath('//li/a/@href')
​
​
for i in range(len(resource_titles)):
	file.write(resource_titles[i]+","+"https://cp-algorithms.com"+resource_links[i][1:]+"\n")

