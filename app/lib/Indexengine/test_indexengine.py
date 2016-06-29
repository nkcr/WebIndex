'''Test the file 'indexengine.py'

Run with `py.test test_indexengine.py`

Author: Noémien Kocher
Licence: MIT
Date: june 2016
'''

import pytest
import indexengine as iengine
from math import log2

def test_settfidf():
    # needed for the total number of documents and the norms
    # here the number of document is 2
    # occurence of word 'wid1' in all documents is 1
    # occurence of word 'wid1' in document 'did1' is 1
    # norms of document 'did1' is arbitrarily 1.4
    repo = {
        'did1': [
            'url', 1.4, {
                'bid1': 'wid1',
                'bid2': 'content2'
            }
        ],
        'did2': [
            'url', 1, {
                'bid1': 'content3',
            }
        ]
    }
    ii = {
        'wid1': [
            0, { # rank
                'did1': [
                    1, 0, { # nbHits, rank
                        'hlid1': [
                            ['bid1', 0, 0] # blockId, positon, domLevel
                        ]
                    }
                ]
            }
        ]
    }
    newrank = (1/1.4)*log2(2/1)
    truth = {
        'wid1': [
            0, {
                'did1': [
                    1, newrank, {
                        'hlid1': [
                            ['bid1', 0, 0] # blockId, positon, domLevel
                        ]
                    }
                ]
            }
        ]
    }
    assert ii != truth
    iengine.settfidf(repo, ii)
    assert ii == truth

def test_setwrank():
    ii = {
        'wid1': [
            0, { # rank
                'did1': [
                    1, 1.9, { # nbHits, rank
                        'hlid1': [
                            ['bid1', 0, 0] # blockId, positon, domLevel
                        ]
                    }
                ],
                'did2': [
                    1, 3.4, { # nbHits, rank
                        'hlid1': [
                            ['bid1', 0, 0] # blockId, positon, domLevel
                        ]
                    }
                ],
                'did3': [
                    1, 2.1, { # nbHits, rank
                        'hlid1': [
                            ['bid1', 0, 0] # blockId, positon, domLevel
                        ]
                    }
                ]
            }
        ],
        'wid2': [
            0, { # rank
                'did9': [
                    1, 1.9, { # nbHits, rank
                        'hlid1': [
                            ['bid1', 0, 0] # blockId, positon, domLevel
                        ]
                    }
                ]
            }
        ]
    }
    truth = {
        'wid1': [
            3.4, { # rank
                'did1': [
                    1, 1.9, { # nbHits, rank
                        'hlid1': [
                            ['bid1', 0, 0] # blockId, positon, domLevel
                        ]
                    }
                ],
                'did2': [
                    1, 3.4, { # nbHits, rank
                        'hlid1': [
                            ['bid1', 0, 0] # blockId, positon, domLevel
                        ]
                    }
                ],
                'did3': [
                    1, 2.1, { # nbHits, rank
                        'hlid1': [
                            ['bid1', 0, 0] # blockId, positon, domLevel
                        ]
                    }
                ]
            }
        ],
        'wid2': [
            1.9, { # rank
                'did9': [
                    1, 1.9, { # nbHits, rank
                        'hlid1': [
                            ['bid1', 0, 0] # blockId, positon, domLevel
                        ]
                    }
                ]
            }
        ]
    }
    assert ii != truth
    iengine.setwrank(ii)
    assert ii == truth

def test_mostranked():
    ii = {
        'wid1': [
            3.4, { # rank
                'did1': [
                    1, 1.9, { # nbHits, rank
                        'hlid1': [
                            ['bid1', 0, 0] # blockId, positon, domLevel
                        ]
                    }
                ],
                'did2': [
                    1, 3.4, { # nbHits, rank
                        'hlid1': [
                            ['bid1', 0, 0] # blockId, positon, domLevel
                        ]
                    }
                ],
                'did3': [
                    1, 2.1, { # nbHits, rank
                        'hlid1': [
                            ['bid1', 0, 0] # blockId, positon, domLevel
                        ]
                    }
                ]
            }
        ],
        'wid2': [
            1.9, { # rank
                'did9': [
                    1, 1.9, { # nbHits, rank
                        'hlid1': [
                            ['bid1', 0, 0] # blockId, positon, domLevel
                        ]
                    }
                ]
            }
        ],
        'wid3': [
            3.1, { # rank
                'did9': [
                    1, 1.9, { # nbHits, rank
                        'hlid1': [
                            ['bid1', 0, 0] # blockId, positon, domLevel
                        ]
                    }
                ]
            }
        ]
    }
    truth = ['wid1','wid3']
    res = iengine.mostranked(2, ii)
    assert res == truth

def test_getcontext():
    repo = {
        'docid': [
            'url1', 2.14, { # url, norms
                1: 'This is content 1',
                2: 'Content 2'
            }
        ],
        'docid2' : [
            'url2', 1.12, {
                1: 'Hello content, how are you?',
                2: 'This is sparta.'
            }
        ]
    }
    ii = {
        'content': [
            12.54, { # rank
                'docid': [
                    2, 12.54, [ # nbHits, rank
                        [ 1, 8, 0, 'p' ], # blockId, position, domLevel, HTML tag
                        [ 2, 0, 0, 'p' ]
                    ]
                ],
                'docid2': [
                    1, 2.32, [
                        [ 1, 6, 0, 'h1' ]
                    ]
                ]
            }
        ]
    }
    keys = ['content']
    offset = 5
    truth = [
        [
            'content', 12.54, [ # wordId, rank
                ['...s is ', '1', 'url1'], # wbefore, wafter, url
                ['...ello ', ' how...', 'url2']
            ]
        ]
    ]
    res = iengine.getcontext(repo, ii, keys, offset)
    assert res == truth
