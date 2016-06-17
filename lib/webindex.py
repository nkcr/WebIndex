import HTMLextraction as parser
from collections import defaultdict
import re

hitlist  = {}
'''Contains the occurences of a word in a document.

{ hitlistId: [ [blockId, position, domLevel], ... ] }
'''
invertedi = {}
'''Inverted Index. Indicated the documents where a word appears.

{ wordId: [ rank, [ [docID, nbHits, rank, hitlistId], ... ] ] }
'''
repository = {}
'''Contains the list of documents that are parsed into blocks

{ docId: [ url, norm, { blockId: content } ] }
'''

def handle_block(content, block_id, html_tag, **kargs):
    docId = 'todo'
    content = content.lower
    content = re.sub(r'\W', ' ', content)
    terms = content.split()

    # ii = Inverted Index
    # hl = hit list
    local_ii = defaultdict(lambda: [ 0, defaultdict(lambda: [0,0, defaultdict(lambda: []) ]) ])
    local_hl = []
    for term in terms:
        hit = [ block_id, kargs['rel_pos'], kargs['dom_level'] ]
        hitlistId = (term,docId)
        local_ii[term][1][docId][2][hitlistId].append(hit)


def handlefile(path):
