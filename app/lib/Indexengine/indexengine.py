'''This module provides functions that interacts with an inverted index.

Author: Noémien Kocher
Licence: MIT
Date: june 2016
'''

from math import log2, log
import operator
import codecs, json
import os
import yaml

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
            idf = log(n / f_t)
            boost = 0
            idl = 0
            for hit in value2[2]:
                local_idl = 1.0 / hit[2]
                if(hit[3] in ['h1', 'h2', 'b', 'figcation', 'strong', 'em', 'h3', 'h4', 'caption']):
                    boost += 1
                if(local_idl > idl):
                    idl = local_idl
            value2[1] = (tf*tf*idf*idl / norms) + boost

def settfidf3(repo, ii):
    '''Update each (word,doc) rank with tf-idf algorithm.
    '''
    for wordid, value in ii.items():
        for docid, value2 in value[1].items():
            f_td = value2[0]
            norms = repo[docid][1]
            n = len(repo)
            f_t = len(value[1])
            tf = f_td
            idf = log(n / f_t)
            boost = 0
            idl = 0
            for hit in value2[2]:
                local_idl = 1.0 / hit[2]
                if(hit[3] in ['h1', 'h2', 'b', 'figcation', 'strong', 'em', 'h3', 'h4', 'caption']):
                    boost += 1
                if(local_idl > idl):
                    idl = local_idl
            value2[1] = (tf*tf*idf / norms) + boost

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

def getcontext(repo, ii, keys, offset=40):
    '''Given the repository, the inverted index and the list of wordId's
    (keys), return an array containing the context of the words in the
    following form:

    [                                      # res
        [                                  # wordoccur
            wordId, rank, [                # dococcurs
                [                          # dococcur
                    rank, url, [           # occurs
                        [wbefore, wafter],
                        ...
                    ]
                ],
                ...
            ]
        ],
        ...
    ]
    The offset is the number of words after and before that will be
    shown.
    '''
    res = []
    for k in keys:
        dococcurs = []
        wordoccur = [k, ii[k][0], dococcurs] # wordId, rank, [occurences]
        # Iterate through each document containing a word, sort keys
        # by individual rank of each document.
        docid_keys = sorted(ii[k][1], key=lambda k2: ii[k][1][k2][1], reverse=True )
        for docid in docid_keys:
            occurs = []
            dococcur = [ ii[k][1][docid][1], repo[docid][0], occurs ] # rank, url, occurs
            for hit in ii[k][1][docid][2]:
                blockid = hit[0]
                position = hit[1]
                starti = position-offset # Start index
                if(starti<0):
                    starti = 0
                endi = position+len(k)+offset # End index
                content = repo[docid][2][blockid] # Get the content block
                wbefore = content[starti:position] # Get few words before
                if(starti > 0):
                    wbefore = '...' + wbefore
                wafter = content[position+len(k)+1:endi] # Get few words after
                if(endi < len(content)):
                    wafter = wafter + '...'
                occurs.append([wbefore,wafter])
            dococcurs.append(dococcur)
        res.append(wordoccur) # Append the occurence to the result
    return res

def savejson(path, data):
    '''Given a path and a data, will save the data as json to the path.
    If a file already exists it will be first deleted.
    '''
    try:
        os.remove(path)
    except OSError:
        pass
    with codecs.open(path, 'w', 'utf8') as f:
        f.write(json.dumps(data, f, ensure_ascii=False, indent=4, sort_keys=True))

def importjson(path):
    '''Given the path of a json file, it will convert it into a dictionary.
    '''
    with codecs.open(path, 'r', 'utf8') as f:
        hash = json.loads(f.read())
    return hash
