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

header = {"Cookie":'aliyungf_tc=AQAAALRyxS6ONAIAUapo393M6yE36JBk; csrfToken=iClmiMJA_4CfYWmPS6XlYIuS; jsid=SEM-SOUGOU-PP-VI-212505; TYCID=376944c0049711eab67d3306471dc5a2; undefined=376944c0049711eab67d3306471dc5a2; ssuid=5267237927; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1573485815; _ga=GA1.2.1223694870.1573485816; _gid=GA1.2.107305798.1573485816; RTYCID=a8d29021bf7343e58115cb78120c92c4; CT_TYCID=fc74c7b544484b239535745a9b1af9f0; bannerFlag=true; token=df048ed7912449dd92ca7367efdbf498; _utm=23c41232e0dc44c782cb47ae8bd044ab; tyc-user-info=%257B%2522claimEditPoint%2522%253A%25220%2522%252C%2522myAnswerCount%2522%253A%25220%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522signUp%2522%253A%25220%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522privateMessagePointWeb%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522%25E8%258C%2582%25E5%2587%25AF%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522privateMessagePoint%2522%253A%25220%2522%252C%2522state%2522%253A%25220%2522%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522isClaim%2522%253A%25220%2522%252C%2522bidSubscribe%2522%253A%2522-1%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522discussCommendCount%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%2522149%2522%252C%2522onum%2522%253A%25220%2522%252C%2522claimPoint%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODI3MDQxNDYyMCIsImlhdCI6MTU3MzUyODExNiwiZXhwIjoxNjA1MDY0MTE2fQ.g04kxJAiPmcLT4R1bCU2cWM4aqhKRCGODWxthPRWk5PdRHx0dEkZdztHWkok34iTNFdgxTdOLKq_Oel-E55MTA%2522%252C%2522pleaseAnswerCount%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252218270414620%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxODI3MDQxNDYyMCIsImlhdCI6MTU3MzUyODExNiwiZXhwIjoxNjA1MDY0MTE2fQ.g04kxJAiPmcLT4R1bCU2cWM4aqhKRCGODWxthPRWk5PdRHx0dEkZdztHWkok34iTNFdgxTdOLKq_Oel-E55MTA; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1573528120; cloud_token=7de4511e690b4cd5865a03825f97fe29; cloud_utm=cff607657e974b5aa693f78f28a5b801',

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