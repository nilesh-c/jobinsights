from items import Profile, ProfileGroup, ProfileCertification, ProfileEducation, ProfileCompany
from scrapy.selector import Selector
from pyquery import PyQuery as pq
from lxml import etree
from StringIO import StringIO

def getProfilePageURLs(response):
	return Selector(response).xpath("//strong/a[contains(@href,'linkedin')]/@href").extract()

def getSearchPageURLs(response):
	return [i.get('href') for i in d('.vcard a[title]:not(.profile-photo)')]

#Quick function to return the profile generated from Response
def parseProfile(response):
	parser = ProfileParser(response.body, response.url)
	parser.parseProfile()
	return parser.profile

class ProfileParser():
	body = None;
	url = None;
	p = None;
	profile = Profile();

	def __init__(self, responseBody, url):
		self.body = responseBody
		self.url = url
		self.p = pq(etree.fromstring(responseBody, parser=etree.HTMLParser()))

	def parseProfile(self):
		self.parseGroups()
		self.parseEducation()
		self.parseExperience()
		self.parseCertification()
		self.parseLanguages()
		self.parsePubCount()
		self.parseBasicInfo()

	def assignIfNotNone(self, key, value):
		if value:
			self.profile[key] = value

	def parseEducation(self):
		education = []
		for i in self.p('.position.education'):
			edu = ProfileEducation()
			if i[0].text.strip() == '':
				edu['url'] = i[0].getchildren()[0].get('href')
				edu['name'] = i[0].getchildren()[0].text.strip()
			else:
				edu['name'] = i[0].text.strip()

			info = i[1].getchildren()
			if len(info) > 0:
				try:
					edu['degree'] = i[1].getchildren()[0].text.strip()
					edu['major'] = i[1].getchildren()[1].text.strip()
				except Exception:
					pass
			periods = i[2].getchildren()
			if len(periods) > 0:
				for period in [p.values() for p in periods[0:2]]: #set dtstart and dtend
					try:
						edu[period[0]] = period[1]
					except Exception:
						pass
			education.append(dict(edu))

		self.assignIfNotNone('education', education)

	def parseExperience(self):
		companies = []
		for i in self.p('.position.experience'):
			company = ProfileCompany()
			posttitle = i.find('div').getchildren()
			try:
				company['role'] = posttitle[0].getchildren()[0].text.strip()
			except Exception:
				pass

			try:
				companyInfo = posttitle[1].getchildren()[0].getchildren()[0]
				if len(companyInfo.getchildren()) > 0:
					children = companyInfo.getchildren()
					company['url'] = companyInfo.get('href')
					company['name'] = companyInfo.getchildren()[0].text.strip()
				else:
					company['name'] = companyInfo.text.strip()
			except Exception:
				pass

			p = pq(i)
			try:
				company['stats'] = p('.orgstats').text().replace("\n", "").replace("\t", "").strip()
			except Exception:
				pass

			if len(p('.period')) > 0:
				periods = p('.period')[0].getchildren()
				if len(periods) > 0:
					for period in [p.values() for p in periods[0:2]]: #set dtstart and dtend
						company[period[0]] = period[1]

			companies.append(company)

		self.assignIfNotNone('companies', companies)

	def parseCertification(self):
		certifications = []
		for i in self.p('.certification'):
			certification = ProfileCertification()
			certification['topic'] = i.find('h3').text.strip()
			try:
				certification['authority'] = i.find('ul').getchildren()[0].text.strip()
			except Exception:
				pass
			try:
				certification['dtstart'] = i.find('ul').getchildren()[1].getchildren()[0].text.strip()
			except Exception:
				pass
			certifications.append(certification)

		self.assignIfNotNone('certifications', certifications)

	def parseGroups(self):
		self.assignIfNotNone('groups', [dict(ProfileGroup(url=i.get('href'), name=i.getchildren()[0].text.strip())) for i in self.p('.group-data').children()])

	def parseSkills(self):
		self.assignIfNotNone('skills', [i.text.strip() for i in self.p('.jellybean')])

	def parseLanguages(self):
		self.assignIfNotNone('languages', [(i.find('h3').text.strip(), i.find('span').text.strip() if i.find('span') is not None else '') for i in self.p('.language')])

	def parsePubCount(self):
		self.assignIfNotNone('publications', len(self.p('.publication')))

	def parseBasicInfo(self):
		self.assignIfNotNone('url', self.url)
		self.assignIfNotNone('first_name', self.p('.given-name').text())
		self.assignIfNotNone('last_name', self.p('.family-name').text())
		self.assignIfNotNone('title', self.p('.headline-title').text())
		self.assignIfNotNone('location', self.p('.locality').text())
		self.assignIfNotNone('industry', self.p('.industry').text())
