'''This module provides functions that interacts with an inverted index.

Author: Noémien Kocher
Licence: MIT
Date: june 2016
'''

from math import log2
import operator
import codecs, json
import os

def settfidf(repo, ii):
    '''Update each (word,doc) rank with tf-idf algorithm.
    '''
    for wordid, value in ii.items():
        for docid, value2 in value[1].items():
            f_td = value2[0]
            norms = repo[docid][1]
            n = len(repo)
            f_t = len(value[1])
            tf = f_td / norms
            idf = log2(n / f_t)
            value2[1] = tf*idf

def settfidf2(repo, ii):
    '''Update each (word,doc) rank with tf-idf algorithm.
    '''
    for wordid, value in ii.items():
        for docid, value2 in value[1].items():
            f_td = value2[0]
            norms = repo[docid][1]
            n = len(repo)
            f_t = len(value[1])
            tf = f_td
            idf = log2(n / f_t)
            boost = 0
            for hit in value2[2]:
                idl = 1.0 / hit[2]
                if(hit[3] in ['h1', 'h2', 'b', 'figcation', 'strong', 'em', 'h3', 'h4', 'cation']):
                    idl += 1
                if(idl > boost):
                    boost = idl
            # if(repo[docid][2][])
            # value2[1] = (tf*idf*idf*boost) / norms
            value2[1] = tf*idf*boost*boost*boost*boost / norms

def setwrank(ii):
    '''Set each word rank with the highest (word,doc) rank.
    '''
    for wordid, value in ii.items():
        for docid, value2 in value[1].items():
            if(value[0] < value2[1]):
                value[0] = value2[1]

def mostranked(quantity, ii):
    '''Retrieve the n most ranked wordId's in an inverted index.
    '''
    keys = sorted(ii, key=lambda k: ii[k][0], reverse=True)
    return keys[:quantity]

def savejson(path, data):
    try:
        os.remove(path)
    except OSError:
        pass
    with codecs.open(path, 'w', 'utf8') as f:
        f.write(json.dumps(data, f, ensure_ascii=False, indent=4, sort_keys=True))
