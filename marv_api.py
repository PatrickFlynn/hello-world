from __future__ import division
import requests
import pandas as pd
import hashlib
import datetime
import math


def APIRequestReturn(resource, offset=None, limit=None):
    publicKey = '38eabd18b8b94ccd28b60885a3ef8f03'
    privateKey = '0cb5c27c64da1fb633b6b483bae95e63d8f2dcb2'
    date = datetime.datetime.now().strftime('%y%m%d%H%M%S%f')
    myhash = hashlib.md5(date+privateKey+publicKey).hexdigest()
    
    payload = {'ts':date, 'apikey':publicKey, 'hash':myhash, 'limit':limit, 'offset':offset}
    headers = {'Accept-Encoding':'gzip'}
    
    url = 'https://gateway.marvel.com:443/v1/public/'
    url = url + resource #'/events?'

    return requests.get(url, headers=headers, params=payload, verify=False)


def retrieveDatasets(url, offset=None, limit=None, max_iterations=100):
    df = pd.DataFrame()
    response = APIRequestReturn(url, offset, limit)
    df = df.append(pd.DataFrame(response.json()['data']['results']))
    
    iterations_needed = int(math.ceil(response.json()['data']['total'] / response.json()['data']['count']))
    
    if iterations_needed > 1:
        counter = response.json()['data']['count']
        if iterations_needed <= max_iterations:
            max_iterations = iterations_needed
        for i in range(0, max_iterations-1):
            response = APIRequestReturn(url, counter, limit)
            df = df.append(pd.DataFrame(response.json()['data']['results']))
            counter += response.json()['data']['count'] 
    df.reset_index(drop=True, inplace=True)
    return df
    
xmen_comics = retrieveDatasets('series/2258/comics?', limit=75, max_iterations=10)


def createStoryColumns(diction):
    test = pd.Series()
    for x in (xmen_comics['stories'].apply(pd.Series)['items'].apply(pd.Series).columns):
        test = test.append(xmen_comics['stories'].apply(pd.Series)['items'].apply(pd.Series)[x].apply(pd.Series))
    test = test.drop(axis=1, columns=[0]).reset_index()
    test = test.dropna()
    test = test.drop_duplicates(subset=['index', 'type'])
    test = test.pivot(index='index', columns='type', values='name')