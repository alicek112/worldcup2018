import requests
from bs4 import BeautifulSoup
import argparse

def get_matches(date, order):

    page = requests.get('http://en.wikipedia.org/wiki/2018_FIFA_World_Cup')
    soup = BeautifulSoup(page.content, 'lxml')

    matches = soup.find_all(itemtype="http://schema.org/SportsEvent")

    todays_matches = []

    for m in matches:
        if m.find(attrs={'class': 'bday dtstart published updated'}).contents[0] == date:
            todays_matches.append(m)


    all_matches = {}

    for match in todays_matches:
        score = match.find('th', style="width: 22%;").string
        names = match.find_all('span', itemprop="name")
        name = names[0].a.string + ' vs ' + names[1].a.string
        
        if score == u'0\u20130':
            print name
        
        score_sum = int(score.split(u'\u2013')[0]) + int(score.split(u'\u2013')[1])
        all_matches[name] = score_sum


    if order:
        print('Matches in order of interest')

        for key, value in sorted(all_matches.iteritems(), key=lambda (k,v): (v,k), reverse=True):
            print key


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Print today\'s matches')
    parser.add_argument('date', help='date in YYYY-MM-DD format')
    parser.add_argument('--order', action='store_true', help='Print matches in order of interest')

    args = parser.parse_args()

    get_matches(args.date, args.order)