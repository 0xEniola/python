#! /usr/bin/python

import requests, bs4, sys, re


def genius(data):
    ''' genius() scans through the google search result of the specified lyrics
        and if there is a result in the page from genius.com, it gets the result from genius.com
    '''

    soup = bs4.BeautifulSoup(data, "html.parser")

    for link in soup.find_all('a', attrs={'href': re.compile('^/url?')}):
        link = link.get('href')[7:]

        if 'genius.com' in link:
            link = re.sub('&.*', '', link) #Strip away garbage parts of the link string that is not a true url(The true url ends before the &).
        
        lyrics = requests.get(link)
        lyrics.raise_for_status()
        
        return lyrics.text
    
    print('No Genius.'); sys.exit()


def arrange(data):
    soup = bs4.BeautifulSoup(data, 'html.parser')

    lSoup = ''
    for this in soup.find_all(class_='Lyrics__Container-sc-1ynbvzw-6 YYrds'):
        lSoup += str(this)

    thisSoup = bs4.BeautifulSoup(lSoup, 'html.parser')
    
    # Unwrap(remove) all div tags in order to display the lyrics perfectly.
    for x in range(str(thisSoup).count('<div')): thisSoup.div.unwrap()
    
    thisSoup = thisSoup.prettify(); thisSoup = thisSoup.split(' ')
    for x in range(len(thisSoup)):
        if thisSoup[x] == '<br/>' and thisSoup[x-1] != '<br/>' and thisSoup[x+1][0] == '[':
            thisSoup.insert(x, '<br/>')
    thisSoup = ' '.join(thisSoup)
    
    #soup = bs4.BeautifulSoup(thisSoup, 'html.parser')
    #return soup.prettify()
    return thisSoup


def writeToFile(data):
    file = open('/home/eniola/Desktop/yoursoul.html', 'w')

    for line in str(data.prettify()):
        file.write(line)
    
    file.close


def main():
    payload = {'q': '%s+lyrics+site:genius.com' %(' '.join(sys.argv[1:]))}
    response = requests.get('https://www.google.com/search', params=payload)
    response.raise_for_status()

    data = genius(response.text)
    lyrics = arrange(data)
    
    soup = bs4.BeautifulSoup(lyrics, 'html.parser')
    print(soup.text)

if __name__ == '__main__': main()
