'''DESCRIPTION HERE

Author: Noémien Kocher
Licence: MIT
Date: june 2016
'''

from collections import defaultdict
import re
import uuid
import codecs
import json
# from nltk.stem.snowball import FrenchStemmer

class BlockExtractor:

    def __init__(self):
        self.ii = defaultdict(lambda: [ 0, defaultdict(lambda: [0,0,[]]) ])
        self.normssq = defaultdict(int)
        self.fr_sw = self.importjson('resources/fr_stop_words.txt')
        self.en_sw = self.importjson('resources/en_stop_words.txt')
        # self.stemmer = FrenchStemmer()

    def update_ii(self, hash, docId):
        for key in hash:
            if(docId in self.ii[key][1]):
                self.ii[key][1][docId][2].extend(hash[key][1][docId][2])
                self.ii[key][1][docId][0] += hash[key][1][docId][0]
            else:
                self.ii[key][1][docId] = hash[key][1][docId]

    def update_norms(self, hash, docId):
        for key, value in hash.items():
            count = value[1][docId][0]
            self.normssq[docId] += count*count

    def handle_block(self, content, block_id, html_tag, **kargs):
        '''Parse a block to an inverted index

        Given a block containing strings, this method tokennize the block and fill
        the inverted index structure.

        For example, given the following block:

            'Lorem-dolor sit dolor'

        returns a hash:
            {
            'lorem':
                [rank,
                    {docId:
                        [nbHit,rank,
                            [ # hitList
                                [blockId,position,domLevel,html_tag],
                                ...
                            ]
                        ]
                    }
                ]
            'dolor': ...
            'sit': ...
            }

        The 'position' takes into account the 'rel_pos' in param and indicates the
        word position into the block.
        If 'rel_pos' equals 10 in params, 'lorem' has position 10, 'dolor' has 16.
        The 'hitListId' is a tuple of (wordId, docId).
        '''
        cur_pos = kargs['rel_pos'] # current position
        docId = kargs['docid']
        content = content.lower()
        terms = re.split('\W', content)

        # ii = Inverted Index
        local_ii = defaultdict(lambda: [ 0, defaultdict(lambda:
             [0,0,[] ]) ])
        for term in terms:
            if(len(term) > 1 and term not in self.fr_sw and term not in self.en_sw):
                # term = self.stemmer.stem(term)
                hit = [ block_id, cur_pos, kargs['dom_level'], str(html_tag) ]
                local_ii[term][1][docId][2].append(hit)
                local_ii[term][1][docId][0] += 1
            cur_pos += 1 + len(term)
        self.update_ii(local_ii, docId)
        self.update_norms(local_ii, docId)
        return (docId, local_ii)

    def importjson(self, path):
        '''Given the path of a json file, it will convert it into a dictionary.
        '''
        with codecs.open(path, 'r', 'utf8') as f:
            hash = json.loads(f.read())
        return hash
