# This script stores all the companny and website data in sqlite database
# And runs accuracy analysis on WebsiteFinder

# Author: Kausal Malladi <kausalmalladi@gmail.com>

import sys
sys.path.append("../")
import whimsy
import csv
import sqlite3
import os.path

csvFilePath = "companies.csv"
databasePath = "whimsy.db"

# Remove previous test database, if any
if os.path.isfile(databasePath) is True:
    os.remove(databasePath)
    print "Removed earlier database"

connection = sqlite3.connect(databasePath)

# To accommodate a lot of non UTF characters that are in the data set
connection.text_factory = str
cursor = connection.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS Websites(company text, website text)')

def analyzeApp():
    total = 0
    correct = 0
    percentage = 0
    cursor.execute('SELECT * FROM Websites')
    for record in cursor.fetchall():
        company = record[0]
        whimsyObj = whimsy.WebsiteFinder()
        url = whimsyObj.searchWeb(company)
        # A few URLs found, have '/' in the end, so removing it
        if url is not None:
            if url.endswith("/"): url = url[:-1]
            url = url.replace("www.", "").replace("https:", "http:")
            urlFromDB = record[1].replace("www.", "").replace("https:", "http:")
            if len(url.split('/')) > 3:
                url = url.rsplit('/', 1)[0]
            if url == urlFromDB:
                correct += 1
            elif url.rsplit('.', 1)[0] == urlFromDB.rsplit('.', 1)[0]:
                correct += 1
        total += 1
        percentage = correct * 100/ total
        print "Accuracy as of now == Correct(", correct,")/Total(", total,") == ", percentage

def storeData(company, website):
    cursor.execute('INSERT INTO Websites VALUES(?, ?)', (company, website))

def loadCSV(csvFilePath):
    with open(csvFilePath, 'rb') as csvFile:
        content = csv.reader(csvFile, delimiter = ',', quotechar = '|')
        for row in content:
            company = ""
            length = len(row)
            # A few entries in the test data set have more than 1 delimiter(,)
            # like "51job, Inc.". This check takes care of it
            if length > 2:
                for item in row[:-1]:
                    company += item
            else:
                company = row[0]
            company = company.strip()
            website = row[length - 1].strip()
            storeData(company, website)

loadCSV(csvFilePath)
print "Loaded CSV and saved all entries to the Database!"
connection.commit()
analyzeApp()
connection.close()
