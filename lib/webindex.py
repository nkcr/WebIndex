import HTMLextraction as parser
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

def handle_block(content, block_id, html_tag, dom_level, is_formatting):
    content = content.lower
    content = re.sub(r'\W', ' ', content)
    terms = content.split()


def handlefile(path):
