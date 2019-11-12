from lxml import etree
import requests
import csv
import time

class Company:
	def __init__(self):
		self.name = ""
		self.tel = ""
		self.email = ""
		self.website = ""
		self.adress = ""
		self.simpleinfo = ""
	def __str__(self):
		return "{},{},{},{},{},{}".format(self.name, self.tel, self.email, self.website, self.adress, self.simpleinfo)

	def toArray(self):
		return [self.name, self.tel, self.email, self.website, self.adress, self.simpleinfo]

header = {"Cookie":'你的 cookie',

		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
		"Referer": "https://www.tianyancha.com/login?from=https%3A%2F%2Fwww.tianyancha.com%2Fcompany%2F866726954"
		}

def getUrlByCompanyName(name):
	'''
	input name output the url of the company
	'''
	url = "https://www.tianyancha.com/search?key=" + name

	r = requests.get(url,headers = header)
	html = etree.HTML(r.text)
	href = html.xpath('//div[@class="search-result-single   "]//a[@class="name "]/@href')

	if len(href) == 0:
		print("获取查询列表失败")
		return False
	else:
		return href[0]

def getCompanyByUrl(url):
	'''
	input the company url output the full html 
	'''
	company = Company()
	r = requests.get(url, headers = header)
	html = etree.HTML(r.text)
	name = html.xpath('//div[@class="content"]//h1[@class="name"]/text()')
	tel = html.xpath('//div[@class="detail "]//div[@class="f0"]/div[1]/span[2]/text()')
	email = html.xpath('//div[@class="detail "]//div[@class="f0"]/div[2]/span[2]/text()')

	website = html.xpath('//div[@class="detail "]//div[@class="f0 clearfix"]/div[1]/span[2]/text()')
	adress = html.xpath('//div[@class="detail "]//div[@class="f0 clearfix"]//div[@class="auto-folder"]/div[1]/text()')
	simpleinfo = html.xpath('//div[@class="detail "]//div[@class="summary"]//text()')

	company.name = "" if len(name) == 0 else name[0]
	company.tel = "" if len(tel) == 0 else tel[0]
	company.email = "" if len(email) == 0 else email[0]
	company.website = "" if len(website) == 0 else website[0]
	company.adress = "" if len(adress) == 0 else adress[0]
	company.simpleinfo = "" if len(simpleinfo) == 0 else simpleinfo[0]
	print(company)
	return company

def getCompaniesByCsv(file):
	companies = []
	with open(file, 'r', encoding= 'utf8') as csvfile:
		lines = csv.reader(csvfile)
		companies = [line[0] for line in lines]
	return companies


def writeToCsvByCompanyies(companies):
	'''
	input companies 
	'''
	with open('output.csv', 'w', encoding='utf8') as csvfile:
		writer = csv.writer(csvfile)
		for company in companies:
			writer.writerow(company.toArray())


def main():
	companies = []
	companynames = getCompaniesByCsv('input.csv')
	for name in companynames:
		time.sleep(10)
		url = getUrlByCompanyName(name)
		company = getCompanyByUrl(url)
		companies.append(company)

	writeToCsvByCompanyies(companies)
		


if __name__ == '__main__':
	main()
