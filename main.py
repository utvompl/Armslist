import csv
from bs4 import BeautifulSoup
from lxml import html
import requests

page = requests.get('http://www.armslist.com/classifieds/search?search=&location=usa&category=all&posttype=7')
 & page=2

soup = BeautifulSoup(page.content, 'html.parser')
for x in soup.find_all("i", class_=True)

soup.find_all("div", class_="info-time")

links = []

csvfile = open("armslist.csv")
csvfilelist = csvfile.read()
