import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from pprint import pprint
import link_lists
import time


client = MongoClient(
    'mongodb+srv://jason:hpkot5NMsCJU!2DivqFx@docbot.ualur.mongodb.net/DocLookup?retryWrites=true&w=majority')
db = client.DocLookup


def python_lookup():
    '''
    Parses all readable text of the id
    in the python documentation website
    and formats it
    '''
    for link in link_lists.python_link_list:
        page = requests.get(link)

        soup = BeautifulSoup(page.content, 'html.parser')

        try:
            dls = soup.find_all('dl')
            for dl in dls:
                doc = ''
                dt = dl.find('dt')
                name = dt.get('id')
                textTags = dl.find_all(['p', 'pre'])
                for tag in textTags:
                    doc += readable_pTag(tag) + readable_preTag(tag)
                python = {
                    'name': name, 'info': doc.rstrip()
                }
                result = db.Python.insert_one(python)
        except:
            pass


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


print(python_lookup())
