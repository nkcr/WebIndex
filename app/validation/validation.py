'''This module provides functions that allowed us to perform validation
of or solution. It provides functions to compute the recall and precision
as well as many others that are used to extract data.

Author: Noémien Kocher
Licence: MIT
Date: june 2016
'''

import codecs
import json
import sys
import glob
import csv
import re
import random
from math import sqrt
from nltk.stem.snowball import FrenchStemmer

sys.path.append('../lib')
import Blockextraction.blockextractor as extractor
import HTMLextraction.htmlextractor as parser
import Indexengine.indexengine as iengine

def importjson(path):
    '''Given the path of a json file, it will convert it into a dictionary.
    '''
    with codecs.open(path, 'r', 'utf8') as f:
        hash = json.loads(f.read())
    return hash

def build_ii(folderpath, savefolder=None):
    '''Given the folder containing the html files, will fill the inverted index
    and repository.
    '''
    engine = extractor.BlockExtractor()
    repo = {}
    files = glob.glob(folderpath + '/*.html')
    for file in files:
        docid = file# + '-' + str(uuid.uuid1())
        blocks = parser.parseHTML(file, docid=docid, callback=engine.handle_block)
        repo[docid] = [ file, sqrt(float(engine.normssq[docid])), blocks ]
    if(savefolder is not None):
        iengine.savejson(savefolder + '/ii.txt', engine.ii)
        iengine.savejson(savefolder + '/repo.txt', repo)
    return(repo,engine.ii)

def rank_tfidf(folderpath, savefolder=None, variant=1):
    '''Given the path of a folder containing 'repo.txt' and 'ii.txt', will set
    ranks according to tfidf and save the repo and inverted index to the given
    folder.
    '''
    repo = importjson(folderpath + '/repo.txt')
    ii = importjson(folderpath + '/ii.txt')
    if(variant is 2):
        iengine.settfidf2(repo,ii)
    elif(variant is 3):
        iengine.settfidf3(repo,ii)
    else:
        iengine.settfidf(repo,ii)
    iengine.setwrank(ii)
    if(savefolder is not None):
        iengine.savejson(savefolder + '/repo.txt', repo)
        iengine.savejson(savefolder + '/ii.txt', ii)
    return ii

def rank_random(folderpath, savefolder=None):
    '''Given the path of a folder containing 'repo.txt' and 'ii.txt', will set
    ranks randomly and save the repo and inverted index to the given
    folder.
    '''
    repo = importjson(folderpath + '/repo.txt')
    ii = importjson(folderpath + '/ii.txt')
    for key in ii:
        ii[key][0] = random.uniform(1,10)
    if(savefolder is not None):
        iengine.savejson(savefolder + '/repo.txt', repo)
        iengine.savejson(savefolder + '/ii.txt', ii)

def compute_zipf(iipath, savepath):
    '''Given the file path of the inverted index, will save statistics about
    zipf's law in the given save path.
    Format of the saved file is in csv, containing the rank and the frequency
    of each word.
    '''
    ii = importii(iipath)
    with open(savepath, 'w') as csvfile:
        spamwriter = csv.writer(csvfile)
        for wordid in ii:
            rank = ii[wordid][0]
            frequency = 0
            for docid in ii[wordid][1]:
                frequency += ii[wordid][1][docid][0]
            spamwriter.writerow([rank,frequency])

def parse_index(path, savepath=None):
    '''This method read the index in csv and save words after removing stop words
    in the save path.
    '''
    fr_sw = importjson('resources/fr_stop_words.txt')
    en_sw = importjson('resources/en_stop_words.txt')
    stemmer = FrenchStemmer()
    index_words = []
    with open(path) as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            content = row[0]
            content = content.lower()
            terms = re.split('\W', content)
            index_words.extend(terms)
    index_words = [
        item for item in index_words # stemmer.stem(item) for item...
        if item not in fr_sw and item not in en_sw and len(item) > 1
    ]
    index_words = list(set(index_words))
    if(savepath is not None):
        iengine.savejson(savepath,index_words)
    print(len(index_words))
    return index_words

def get_best_words(quantity, iipath, savepath=None):
    '''Return the n best words given the path of the inverted index. Save them
    in a file if a save path is given.
    '''
    ii = importjson(iipath)
    keys = iengine.mostranked(quantity, ii)
    if(savepath is not None):
        iengine.savejson(savepath, keys)
    return keys

# def compute_recall(indexwordspath, bestwordspath):
#     '''Compute the recall given the path of the index and the path of the best
#     words.
#     '''
#     index = importjson(indexwordspath)
#     best_words = importjson(bestwordspath)
#     recall = compute_recall(index, best_words)
#     print(recall*100, '%')
#     return recall

# python3 -c "import main; main.compute_full_recall(main.rank_tfidf,'ii-base','ii-tfidf2',2,1000)"
def compute_full_recall(rank_func, sourcefolder, savefolder, variant, quantity=10000):
    '''This function is a shortcut to directly rank an inverted index, get the
    best words and compute the recall.
    The 'rank_func' takes as parameter 'sourcefolder, savefolder, variant'
    Will output the file containing the best words and the file to plot the recall.
    '''
    rank_func(sourcefolder, savefolder, variant)
    best_words_path = savefolder + '/best' + str(quantity) + '.txt'
    get_best_words(quantity, savefolder+'/ii.txt', best_words_path)
    # compute_recall('resources/index_words.txt', best_words_path)
    compute_graph_recall('resources/index_words.txt', best_words_path, savefolder + '/graph_recall_' + str(quantity) + '.csv')

def compute_recall(indexwords, bestwords):
    '''Given the index of words en the words found, compute and return the recall.
    Recall is TP / (TP+FN)
    '''
    true_positive = len( set(indexwords).intersection(bestwords) )
    false_negative = len ( set(indexwords).difference(bestwords) )
    recall = true_positive / ( true_positive + false_negative )
    return recall

# python3 -c "import main; main.compute_graph_recall('resources/index_words.txt', 'ii-tfidf2/best10000.txt', 'ii-tfidf2/graph_recall_10000.csv')"
def compute_graph_recall(indexwordspath, bestwordspath, savepath):
    '''Given the path of the index words and the path of the words found,
    will compute the recall from 0 the the number of words found and save it as
    a csv file in the savepath.
    '''
    index = importjson(indexwordspath)
    best_words = importjson(bestwordspath)
    total = 0
    with open(savepath, 'w') as csvfile:
        spamwriter = csv.writer(csvfile)
        for i in range(0, len(best_words)):
            recall = compute_recall(index,best_words[:i])
            row = [i,recall]
            total += recall
            spamwriter.writerow(row)
    print("Total recall: ", total)

# python3 -c "import main; main.compute_total_recall('ii-tfidf2/graph_recall_10000.csv', 7814)"
def compute_cumulated_recall(recallpath, quantity):
    '''Given the path of a recall stats csv, will compute the comulated total
    until the given quantity.
    '''
    index_words = []
    i = 0
    total = 0
    with open(recallpath) as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            if(i < quantity):
                total += float(row[1])
            i += 1
    print(total)
    return total

def compute_precision(indexwords, bestwords):
    '''Given the index of words en the words found, compute and return the precision.
    Precision is TP / (TP+FP)
    '''
    true_positive = len( set(indexwords).intersection(bestwords) )
    false_positive = len ( set(bestwords).difference(indexwords) )
    if(true_positive+false_positive == 0):
        return 1
    precision = true_positive / ( true_positive + false_positive )
    return precision

# python3 -c "import main; main.compute_graph_precision('resources/index_words.txt', 'ii-tfidf2/best10000.txt', 'ii-tfidf2/graph_precision_10000.csv')"
def compute_graph_precision(indexwordspath, bestwordspath, savepath):
    '''Given the path of the index words and the path of the words found,
    will compute the precision from 0 the the number of words found and
    save it as a csv file in the savepath.
    '''
    index = importjson(indexwordspath)
    best_words = importjson(bestwordspath)
    total = 0
    with open(savepath, 'w') as csvfile:
        spamwriter = csv.writer(csvfile)
        for i in range(0, len(best_words)):
            precision = compute_precision(index,best_words[:i])
            row = [i,precision]
            total += precision
            spamwriter.writerow(row)
    print("Total precision: ", total)
