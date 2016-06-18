'''DESCRIPTION HERE

Author: Noémien Kocher
Licence: MIT
Date: june 2016
'''

from collections import defaultdict
import re
import uuid

class BlockExtractor:

    def __init__(self):
        self.ii = defaultdict(lambda: [ 0, defaultdict(lambda:
             [0,0, defaultdict(lambda: []) ]) ])

    def update_ii(self, hash, docId):
        for key, value in hash.items():
            self.ii[key][1][docId] = value[1][docId]

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
                            {hitListId:
                                [
                                    [blockId,position,domLevel],
                                    ...
                                ]
                            }
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
             [0,0, defaultdict(lambda: []) ]) ])
        for term in terms:
            if(term is not ''):
                hit = [ block_id, cur_pos, kargs['dom_level'] ]
                hitlistId = (term,docId)
                local_ii[term][1][docId][2][hitlistId].append(hit)
            cur_pos += 1 + len(term)
        self.update_ii(local_ii, docId)
        return (docId, local_ii)
