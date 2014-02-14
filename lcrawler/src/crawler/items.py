from scrapy.item import Item, Field


class Profile(Item):
    url = Field()
    first_name = Field()
    last_name = Field()
    title = Field()
    location = Field()
    industry = Field()
    skills = Field() #list of skills
    companies = Field() #list of ProfileCompany
    education = Field() #list of ProfileEducation
    groups = Field() #list of ProfileGroup
    languages = Field() #list of languages and proficiencies
    certifications = Field() #list of ProfileCertification
    publications = Field() #number of publications

class ProfileGroup(Item):
    url = Field()
    name = Field()

class ProfileCertification(Item):
    topic = Field()
    authority = Field()
    dtstart = Field()

class ProfileEducation(Item):
    url = Field()
    name = Field()
    degree = Field()
    major = Field()
    dtstart = Field()
    dtend = Field()
    dtstamp = Field()

class ProfileCompany(Item):
    url = Field()
    name = Field()
    role = Field()
    dtstart = Field()
    dtend = Field()
    dtstamp = Field()
    stats = Field()

class Company(Item):
    url = Field()
    name = Field()
    industry = Field()
    type = Field()
    employees = Field()