import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from dotenv import load_dotenv
import link_lists
import os

load_dotenv()

MONGO = os.getenv('MONGODBDOC')

client = MongoClient(MONGO)

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
                # check to see if difference update if there is anything new
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


def javascript_lookup():
    for link in link_lists.javascript_link_list:
        try:
            page = requests.get(link)

            soup = BeautifulSoup(page.content, 'html.parser')
            artice = soup.find('article')
            div = artice.find('div')

            name = soup.find('h1').text
            pTags = div.find('p')
            javascript = {
                'name': name, 'info': pTags.text.rstrip()
            }
            result = db.JavaScript.insert_one(javascript)
        except:
            pass
