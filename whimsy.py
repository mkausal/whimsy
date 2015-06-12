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
import string
from socket import error as SocketError

max_results = 10
wiki_xml_file = "wikiData.xml"
stop_words = stopwords.words("english")

class WebsiteFinder:
    def crawlWiki(self, company):
        company.replace(" ","%20")
        url = "http://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=xml&titles="+ company +"&rvsection=0"
        try:
            xmlData = urllib.urlopen(url).read()
        except:
            return "socket error"
        f = open(wiki_xml_file, "w")
        f.write(xmlData)
        f.close()
        tree = ET.parse(wiki_xml_file)
        root = tree.getroot()
        for text in root.itertext():
            try:
                url = text.lower().split('url|')[1].split('|')[0]
                return url
            except IndexError:
                return "no wiki"
        return "no wiki"

    def removeStopWords(self, text):
        text = ' '.join([word for word in text.split() if word not in stop_words])
        return text

    def crawl(self, url, company):
        try:
            content = urllib.urlopen(url).read()
        except:
            return "socket error"
        try:
            # Trying to extract title, if it exists
            webpage_title = content.lower().split('<title>')[1].split('</title>')[0]
            if "Access Denied".lower() in webpage_title: return "access denied"
            company = self.removeStopWords(company).lower()
            webpage_title = self.removeStopWords(webpage_title).lower()
            exclude = set(string.punctuation)
            company = ''.join(ch for ch in company if ch not in exclude)
            webpage_title = ''.join(ch for ch in webpage_title if ch not in exclude)
            if company not in webpage_title:
                companySplit = company.split(' ')
                companySplit = [item.lower() for item in companySplit]
                webpageSplit = webpage_title.split(' ')
                webpageSplit = [item.lower() for item in webpageSplit]
                if set(companySplit) & set(webpageSplit) is not None:
                    return "domain found"
                return "title mismatch"
            return "domain found"
        except IndexError:
            return "no title"

    def searchWeb(self, company):
        count = 0
        for url in search(company + "website", stop=max_results):
            if "en.wikipedia.org" in url: continue
            crawl_url_result = self.crawl(url, company)
            if (crawl_url_result == "access denied" or crawl_url_result == "no title"):
                # If first result is not crawlable or title is not mentioned
                # most probably it is the right domain and hence check Wikipedia
                if count == 0:
                    count += 1
                    crawl_wiki_result = self.crawlWiki(company)
                    # If Wikipedia has an entry, return the URL
                    # else continue crawling further results from Google search
                    if (crawl_wiki_result == "no wiki" or crawl_wiki_result == "socket error"):
                        continue
                    else:
                        return crawl_wiki_result
            elif crawl_url_result == "title mismatch":
                continue
            elif crawl_url_result == "socket error":
                continue
            else:
                # domain found
                return url
