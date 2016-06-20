'''Test the file 'blockextractor.py'

Run with `py.test test_extractor.py`

Author: Noémien Kocher
Licence: MIT
Date: june 2016
'''

import pytest
import blockextractor as parser

# Test the parsing of a block with the method 'handle_block'
def test_handleblock():
    content = 'Lorèm-dolor sit dolor'
    block_id = 12
    html_tag = 'p'
    rel_pos = 10
    dom_level = 3
    path = 'path'
    docId = 'docid'

    truth = {
        'lorèm': [ # wordId
            0, {   # rank
                docId: [1, 0, {  # nbHits, rank
                    ('lorèm',docId): [ # hitlistId
                        [12,10,3] # blockId, position, domLevel
                    ]
                }]
            }
        ],
        'dolor': [
            0, {
                docId: [2, 0, {
                    ('dolor',docId): [
                        [12,16,3],
                        [12,26,3]
                    ]
                }]
            }
        ],
        'sit': [
            0, {
                docId: [1, 0, {
                    ('sit',docId): [
                        [12,22,3]
                    ]
                }]
            }
        ]
    }
    engine = parser.BlockExtractor()
    (_, res) = engine.handle_block(content, block_id, html_tag,
        dom_level=dom_level, rel_pos=rel_pos, path=path, docid=docId)
    assert res == truth

# Test the case of an update of the inverted index with method 'update_ii'
def test_update_ii():
    ii = {
        'tree': [ 0, { # rank
            'did1': [ 2, 0, { # nbHit, rank
                ('tree', 'did1'): [  # the hitlist
                    ['bid1', 12, 1], # blockId, position, domLevel
                    ['bid2', 10, 2]
                ]
            } ],
            'did2': [ 1, 0, {
                ('tree', 'did2'): [
                    ['bid1', 1, 3]
                ]
            } ]
        } ],
        'cat': [ 0, {
            'did1': [ 1, 0, {
                ('cat', 'did1'): [
                    ['bid1', 30, 1]
                ]
            } ]
        } ]
    }
    local_ii = {
        'tree': [ 0, {
            'did3': [ 2, 0, {
                ('tree', 'did2'): [
                    ['bid1', 200, 12],
                    ['bid2', 10, 13]
                ]
            } ]
        } ],
        'cat': [ 0, {
            'did3': [ 3, 0, {
                ('cat', 'did2'): [
                    ['bid1', 200, 12],
                    ['bid2', 10, 13],
                    ['bid3', 15, 13]
                ]
            } ]
        } ]
    }
    truth = {
        'tree': [ 0, { # rank
            'did1': [ 2, 0, { # nbHit, rank
                ('tree', 'did1'): [  # the hitlist
                    ['bid1', 12, 1], # blockId, position, domLevel
                    ['bid2', 10, 2]
                ]
            } ],
            'did2': [ 1, 0, {
                ('tree', 'did2'): [
                    ['bid1', 1, 3]
                ]
            } ],
            'did3': [ 2, 0, {
                ('tree', 'did2'): [
                    ['bid1', 200, 12],
                    ['bid2', 10, 13]
                ]
            } ]
        } ],
        'cat': [ 0, {
            'did1': [ 1, 0, {
                ('cat', 'did1'): [
                    ['bid1', 30, 1]
                ]
            } ],
            'did3': [ 3, 0, {
                ('cat', 'did2'): [
                    ['bid1', 200, 12],
                    ['bid2', 10, 13],
                    ['bid3', 15, 13]
                ]
            } ]
        } ]
    }
    engine = parser.BlockExtractor()
    engine.ii = ii
    assert engine.ii != truth
    engine.update_ii(local_ii, 'did3')
    assert engine.ii == truth

# Update with an empty hash should not change the inverted index
def test_empty_param_update():
    ii = {
        'tree': [ 0, { # rank
            'did1': [ 2, 0, { # nbHit, rank
                ('tree', 'did1'): [  # the hitlist
                    ['bid1', 12, 1], # blockId, position, domLevel
                    ['bid2', 10, 2]
                ]
            } ],
            'did2': [ 1, 0, {
                ('tree', 'did2'): [
                    ['bid1', 1, 3]
                ]
            } ]
        } ],
        'cat': [ 0, {
            'did1': [ 1, 0, {
                ('cat', 'did1'): [
                    ['bid1', 30, 1]
                ]
            } ]
        } ]
    }
    local_ii = {}
    engine = parser.BlockExtractor()
    engine.ii = ii
    assert engine.ii == ii
    engine.update_ii(local_ii, 'did3')
    assert engine.ii == ii

# Test the first update, when the inverted index is empty
def test_empti_ii_update():
    local_ii = {
        'tree': [ 0, {
            'did3': [ 2, 0, {
                ('tree', 'did2'): [
                    ['bid1', 200, 12],
                    ['bid2', 10, 13]
                ]
            } ]
        } ],
        'cat': [ 0, {
            'did3': [ 2, 0, {
                ('cat', 'did2'): [
                    ['bid1', 200, 12],
                    ['bid2', 10, 13],
                    ['bid3', 15, 13]
                ]
            } ]
        } ]
    }
    engine = parser.BlockExtractor()
    assert engine.ii != local_ii
    engine.update_ii(local_ii, 'did3')
    assert engine.ii == local_ii

def test_existing_update():
    ii = {
        'tree': [ 0, { # rank
            'did1': [ 2, 0, { # nbHit, rank
                ('tree', 'did1'): [  # the hitlist
                    ['bid1', 12, 1], # blockId, position, domLevel
                    ['bid2', 10, 2]
                ]
            } ],
            'did2': [ 1, 0, {
                ('tree', 'did2'): [
                    ['bid1', 1, 3]
                ]
            } ]
        } ],
        'cat': [ 0, {
            'did1': [ 1, 0, {
                ('cat', 'did1'): [
                    ['bid1', 30, 1]
                ]
            } ]
        } ]
    }
    local_ii = {
        'tree': [ 0, {
            'did2': [ 2, 0, {
                ('tree', 'did2'): [
                    ['bid1', 200, 12],
                    ['bid2', 10, 13]
                ]
            } ]
        } ],
        'cat': [ 0, {
            'did2': [ 3, 0, {
                ('cat', 'did2'): [
                    ['bid1', 200, 12],
                    ['bid2', 10, 13],
                    ['bid3', 15, 13]
                ]
            } ]
        } ]
    }
    truth = {
        'tree': [ 0, { # rank
            'did1': [ 2, 0, { # nbHit, rank
                ('tree', 'did1'): [  # the hitlist
                    ['bid1', 12, 1], # blockId, position, domLevel
                    ['bid2', 10, 2]
                ]
            } ],
            'did2': [ 2, 0, {
                ('tree', 'did2'): [
                    ['bid1', 200, 12],
                    ['bid2', 10, 13]
                ]
            } ]
        } ],
        'cat': [ 0, {
            'did1': [ 1, 0, {
                ('cat', 'did1'): [
                    ['bid1', 30, 1]
                ]
            } ],
            'did2': [ 3, 0, {
                ('cat', 'did2'): [
                    ['bid1', 200, 12],
                    ['bid2', 10, 13],
                    ['bid3', 15, 13]
                ]
            } ]
        } ]
    }
    engine = parser.BlockExtractor()
    engine.ii = ii
    assert engine.ii != truth
    engine.update_ii(local_ii, 'did2')
    assert engine.ii == truth

def test_norms_update():
    docid = 'did2'
    ii = {
        'tree': [ 0, {
            docid: [ 2, 0, {
                ('tree', docid): [
                    ['bid1', 200, 12],
                    ['bid2', 10, 13]
                ]
            } ]
        } ],
        'cat': [ 0, {
            docid: [ 3, 0, {
                ('cat', docid): [
                    ['bid1', 200, 12],
                    ['bid2', 10, 13],
                    ['bid3', 15, 13]
                ]
            } ]
        } ]
    }
    engine = parser.BlockExtractor()
    engine.ii = ii
    assert engine.normssq[docid] == 0
    engine.update_norms(ii, docid)
    assert engine.normssq[docid] == 9+4
