#!/usr/bin/env python

# Whimsy, as the name indicates, is a crazy application
# that takes input as a company name and gives it's URL

# Author: Kausal Malladi <kausalmalladi@gmail.com>

import whimsy

whimsyObj = whimsy.WebsiteFinder()
while True:
    company = raw_input("Enter a company name: ")
    domain = whimsyObj.searchWeb(company)
    print domain
