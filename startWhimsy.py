#!/usr/bin/env python

# Whimsy, as the name indicates, is a crazy application
# that takes input as a company name and outputs it's
# website URL. This application uses Google API
# for fetching search results.

# This app also tries to parse Wikipedia's InfoBox if
# a web page is not accessible or returns "Access Denied".

# This app uses NLTK library to remove stopwords from
# input query and also from Web page title, for better results.

# Author: Kausal Malladi <kausalmalladi@gmail.com>

from google import search
import urllib
import xml.etree.ElementTree as ET
from nltk.corpus import stopwords

max_results = 10
wiki_xml_file = "wikiData.xml"
stop_words = stopwords.words("english")

def crawlWiki(company):
    company.replace(" ","%20")
    url = "http://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=xml&titles="+company+"&rvsection=0"
    xmlData = urllib.urlopen(url).read()
    f = open(wiki_xml_file, "w")
    f.write(xmlData)
    f.close()
    tree = ET.parse(wiki_xml_file)
    root = tree.getroot()
    for text in root.itertext():
        print text.lower().split('url|')[1].split('|')[0]
    return True

def removeStopWords(text):
    text = ' '.join([word for word in text.split() if word not in stop_words])
    return text

def crawl(url, company):
    content = urllib.urlopen(url).read()
    try:
        # Trying to extract title, if it exists
        webpage_title = content.lower().split('<title>')[1].split('</title>')[0]
    except IndexError:
        return crawlWiki(company)
    if "Access Denied".lower() in webpage_title: return crawlWiki(company)
    company = removeStopWords(company)
    webpage_title = removeStopWords(webpage_title)
    if company.lower() not in webpage_title: return False
    return True

def searchWeb(company):
    for url in search(company + "website", stop=max_results):
        if (crawl(url, company) is True):
            print url
            break

while True:
    company = raw_input("Enter a company name: ")
    searchWeb(company)
