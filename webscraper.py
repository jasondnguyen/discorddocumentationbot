import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from print import pprint


URL = 'https://docs.python.org/3/library/functions.html'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

connection_url = 'mongodb+srv://jason:hpkot5NMsCJU!2DivqFx@docbot.ualur.mongodb.net/<dbname>?retryWrites=true&w=majority'


def python_lookup():
    '''
    Parses all readable text of the id
    in the python documentation website
    and formats it
    '''
    doc = ''
    dls = soup.find_all('dl')
    for dl in dls:
        print(dl.find('dt').get('id'))
        textTags = dl.find_all(['p', 'pre'])
        for tag in textTags:
            doc += readable_pTag(tag) + readable_preTag(tag)
        return doc


def readable_pTag(textTag):
    '''
    Returns all the text formatted if
    a pTag has been pass through
    '''
    if textTag.name == 'p':
        return textTag.text.replace('\n', '') + '\n\n'
    return ''


def readable_preTag(textTag):
    '''
    Returns all the text formatted if
    a preTag has been pass through
    '''
    if textTag.name == 'pre':
        return "```" + textTag.text.rstrip() + "```"
    return ''


# pTags = function.find_all('p')
#  for tag in pTags:
#       if function.find(id=id):
#            try:
#                 pre = "\n```" + function.find('pre').text.rstrip() + "```"
#             except AttributeError:
#                 pre = ""
#             return tag.text.replace('\n', '') + pre
