from lxml import html
import requests

file = open("D:\\Logical_Reasoning.txt", 'a+')
page = requests.get("https://www.indiabix.com/logical-reasoning/questions-and-answers/")

tree = html.fromstring(page.content)

problems = tree.xpath('//div[@class="div-topics-index"]/ul//*/text()')
links = tree.xpath('//div[@class="div-topics-index"]/ul//*/@href') 

for p, l in zip(problems, links):
	file.write(p+",https://www.indiabix.com"+l+"\n")
