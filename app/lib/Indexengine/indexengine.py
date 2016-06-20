'''This module provides functions that interacts with an inverted index.

Author: Noémien Kocher
Licence: MIT
Date: june 2016
'''

from math import log
import operator

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
            idf = log(n / f_t)
            value2[1] = tf*idf

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
