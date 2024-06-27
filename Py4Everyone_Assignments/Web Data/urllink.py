# To run this, download the BeautifulSoup zip file
# http://www.py4e.com/code3/bs4.zip
# and unzip it in the same directory as this file

import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = input('Enter URL: ')
count = input("Enter count: ")
position = input("Enter position: ")

html = urllib.request.urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, 'html.parser')

# Retrieve all of the anchor tags
print("Retrieving",url)
tags = soup('a')
for i in range(int(count)):
    links = []
    for tag in tags:
        links.append(str(tag.get('href', None)))
    html = urllib.request.urlopen(links[int(position)-1], context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')
    print("Retrieving",links[int(position)-1])
    tags = soup('a')