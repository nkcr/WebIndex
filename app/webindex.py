'''
Author: Noémien Kocher
Licence: MIT
Date: june 2016
'''

import lib.HTMLextraction.htmlextractor as parser
import lib.Blockextraction.blockextractor as blockextractor
import lib.Indexengine.indexengine as iengine
import uuid
import csv
import glob
from math import sqrt

class Webindex:
    '''This class provides an interface between the Flask webserver
    and the module Blockextraction, HTMLextraction and Indexengine.
    '''

    def __init__(self):
        self.engine = blockextractor.BlockExtractor()
        self.repo = {}
        self.ii = {}

    def handlefile(self, path):
        '''Parse a file to blocks and tokenize each block filling the inverted index.
        Also updates the repo data structure.
        '''
        docid = path# + '-' + str(uuid.uuid1())
        blocks = parser.parseHTML(path, docid=docid, callback=self.engine.handle_block)
        self.repo[docid] = [ path[7:], sqrt(float(self.engine.normssq[docid])), blocks ]

    def update(self, quantity=10):
        '''Compute the tf-idf and update word ranks. Return the n best words.
        '''
        iengine.settfidf2(self.repo,self.engine.ii)
        iengine.setwrank(self.engine.ii)
        best = iengine.mostranked(quantity,self.engine.ii)
        self.ii = self.engine.ii
        return best

    def mostranked(self, quantity=10):
        '''Retreive the n best words with their contexts.
        '''
        keys = self.update(quantity)
        return iengine.getcontext(self.repo, self.ii, keys)

    def saveii(self):
        '''Save the inverted index to 'data/ii.txt'.
        '''
        iengine.savejson('data/ii.txt', self.ii)

    def saverepo(self):
        '''Save the repository to 'data/repo.txt'.
        '''
        iengine.savejson('data/repo.txt', self.repo)

    def read_mostranked(self, quantity=100):
        '''Try to load data-structures in 'data' folder and return
        n best words.
        '''
        try:
            ii = iengine.importjson('data/ii.txt')
            repo = iengine.importjson('data/repo.txt')
        except OSError:
            return {}
        self.ii = ii
        keys = iengine.mostranked(quantity, ii)
        return iengine.getcontext(repo, ii, keys)

    def bias(self, word, biasv):
        '''Change the rank of a word.
        '''
        try:
            ii = iengine.importjson('data/ii.txt')
        except OSError:
            return {}
        ii[word][0] *= (biasv)
        iengine.savejson('data/ii.txt', ii)

    def get_words(self):
        '''Return all the words in the inverted index.
        '''
        return iengine.words(self.ii)

# webindex = Webindex()
# files = glob.glob('documents/TIF_FR/*.html')
# for file in files:
#     webindex.handlefile(file)
# webindex.savestats('test.csv')
