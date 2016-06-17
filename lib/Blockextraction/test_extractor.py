import pytest
import blockextractor as parser

def test_handleblock():
    content = 'Lorèm-dolor sit dolor'
    docId = 'todo'
    block_id = 12
    html_tag = 'p'
    rel_pos = 10
    dom_level = 3
    truth = {
        'lorèm': [ # wordId
            0, {   # rank
                'todo': [0, 0, {  # docId, nbHits, rank
                    ('lorèm','todo'): [ # hitlistId
                        [12,10,3] # blockId, position, domLevel
                    ]
                }]
            }
        ],
        'dolor': [
            0, {
                'todo': [0, 0, {
                    ('dolor','todo'): [
                        [12,16,3],
                        [12,26,3]
                    ]
                }]
            }
        ],
        'sit': [
            0, {
                'todo': [0, 0, {
                    ('sit','todo'): [
                        [12,22,3]
                    ]
                }]
            }
        ]
    }
    res = parser.handle_block(content, block_id, html_tag,
        dom_level=dom_level, rel_pos=rel_pos)
    assert res == truth
