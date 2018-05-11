#!/usr/bin/env python

"""Get all page names of a given language."""

import json
import requests


def query(lang, query):
    query = "&".join(query)
    q = (u"https://{lang}.wikipedia.org/w/api.php?action=query&{query}"
         "&format=json"
         .format(lang=lang, query=query))
    r = requests.get(q)
    return json.loads(r.text)


def get_all_page_titles(lang, apcontinue='', max_pages=float('inf')):
    page_titles = []
    apcontinue = True
    q = ["list=allpages", "aplimit=2", "apcontinue={}".format(apcontinue)]
    while apcontinue:
        result = query(lang, q)
        print(result['query']['allpages'][0])
        page_titles += [(p['title'], p['pageid'])
                        for p in result['query']['allpages']]
        if 'continue' not in result:
            print("continue not in result")
            apcontinue = None
            break
        apcontinue = result['continue']['apcontinue']
        q[2] = u"apcontinue={}".format(apcontinue)
        if len(page_titles) > max_pages:
            print("max_pages reached")
            break
    return {'page_titles': page_titles, 'continue': apcontinue}


lang = 'cy'
page_titles = get_all_page_titles(lang)
print(len(page_titles['page_titles']))
print(page_titles['continue'])
