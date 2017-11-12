import csv
from bs4 import BeautifulSoup
from lxml import html
import requests

states = ['alabama', 'alaska', 'arizona', 'arkansas', 'california', 'colorado', 'connecticut', 'delaware',\
 'florida', 'georgia', 'hawaii', 'idaho', 'illinois', 'indiana', 'iowa', 'kansas', 'kentucky', 'louisiana',\
  'maine', 'maryland', 'massachusetts', 'michigan', 'minnesota', 'mississippi', 'missouri', 'montana', 'nebraska',\
   'nevada', 'new-hampshire', 'new-jersey', 'new-mexico', 'new-york', 'north-carolina', 'north-dakota', 'ohio',\
    'oklahoma', 'oregon', 'pennsylvania', 'rhode-island', 'south-carolina', 'south-dakota', 'tennessee', 'texas',\
     'utah', 'vermont', 'virginia', 'washington', 'west-virginia', 'wisconsin', 'wyoming']

url = "http://www.armslist.com"

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'}
def main():
    with open('data.csv', 'w', newline='', encoding = 'UTF-8') as f:
        thewriter = csv.writer(f)
 
        for i in states:
            query(i, thewriter)
    return 0

def query(location, thewriter):
    '''
        Function for states
    '''
    # Load initial query page
    page = requests.get('%s/classifieds/search?location=%s&category=guns&posttype=7&ships=False' % (url, location), headers = headers)

    # Page Parser
    soup = BeautifulSoup(page.content, 'html.parser')

    pagerange = 3 #int(soup.ul.findall('li')[-2].a.string)
    for i in range(1, pagerange+1):
        page = requests.get('%s/classifieds/search?location=%s&category=guns&posttype=7&ships=False&page=%d' % (url, location, i), headers = headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        for ref in soup.find_all('div', href = True):
            scrape(ref['href'], location, thewriter)
    return 0


def scrape(ref, location, thewriter):
    '''
        Function for listings
    '''
    if ref == None:
        return -1
    page = requests.get('%s%s' % (url, ref), headers = headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    price = 'N/A'
    trade_type = 'N/A'
    listed_on = 'N/A'
    post_id = 'N/A'

    # for in individual listings
    for i in soup.find_all('span', class_={'user-id', 'price', 'date'}):
        if i.string[2] == '$':
            trade_type = "Sell/Trade"
            price = i.string[4:]

        elif i.string == "Offer":
            price = '.'
            trade_type = "Buy"

        elif i.string[:10] == 'Listed On:':
            listed_on = i.string[10:]

        elif i.string[:8] == 'post id:':
            post_id = i.string[8:]

    category = 'N/A'
    manufacturer = 'N/A'
    action = 'N/A'

    # for getting category in individual listings
    for i in soup.find_all('ul', class_='category'):
        for j in i.find_all('li'):
            li_s = j.find_all('span')
            if li_s[0].string == 'CATEGORY':
                category = li_s[1].string
            elif li_s[0].string == "Manufacturer":
                manufacturer = li_s[1].string[2:]
            elif li_s[0].string == "Action":
                action = li_s[1].string[2:]

    description = 'N/A'
    for k in soup.find_all('div', class_='postContent'):
        description = k.get_text(strip = True)


    title = 'N/A'
    title = soup.find_all('h1')[0].string
    thewriter.writerow([title, trade_type, price, location, post_id, listed_on, category, manufacturer, action, description])
    return 0

main()
