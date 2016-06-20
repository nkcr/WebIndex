'''Test the file 'htmlextractor'

Run with `py.test test_extractor.py`

Author: Noémien Kocher
Licence: MIT
Date: june 2016
'''

import pytest
import htmlextractor as parser
import os

files_root = os.path.abspath('test_files') + '/'

def test_empty():
    truth = {}
    assert parser.parseHTML(files_root + 'empty.html') == truth

def test_no_content():
    truth = {}
    assert parser.parseHTML(files_root + 'no_content.html') == truth

def test_simple():
    truth = {1: 'Title', 2: 'Content'}
    assert parser.parseHTML(files_root + 'simple.html') == truth

def test_nested_blocks():
    truth = {
        1: 'Title',
        2: 'This', 3: 'is', 4: 'so', 5: 'nested!',
        6: 'Not', 7: 'that', 8: 'hard', 9: 'indeed.'
    }
    assert parser.parseHTML(files_root + 'nested_blocks.html') == truth

def test_formatting_blocks():
    truth = {
        1: 'Title',
        2: 'Tags can highlight important elements .'
    }
    assert parser.parseHTML(files_root + 'formatting_blocks.html') == truth

def test_nested_formatting():
    truth = {
        1: 'Title',
        2: 'Tags can be nested . This makes me happy.'
    }
    assert parser.parseHTML(files_root + 'nested_formatting.html') == truth

def test_special_formatting():
    truth = {
        1: 'Title',
        2: 'a1 a2 a3 a4 a5 a6 a7 a8',
        3: 'a9',
        4: 'a10'
    }
    assert parser.parseHTML(files_root + 'special_formatting.html') == truth

def test_full_content():
    truth = {
        1: 'Title',
        2: 'a1', 3: 'a2',
        4: 'c1 c2 c3 c4',
        5: 'a3', 6: 'a4', 7: 'a5', 8: 'a6', 9: 'a7 a8',
        10: 'a9', 11: 'a10', 12: 'a11 a12 b13',
        13: 'a13', 14: 'a14 a15 a16 b17 a17',
        15: 'e1', 16: 'e2', 17: 'e3', 18: 'e4',
        19: 'e5', 20: 'e6', 21: 'e7', 22: 'e8 e9 e10 e11'
    }
    assert parser.parseHTML(files_root + 'full_content.html') == truth

def test_utf8_content():
    truth = {
        1: 'Title',
        2: 'é à ü'
    }
    assert parser.parseHTML(files_root + 'utf8_content.html') == truth

def test_callback():
    source = files_root + 'normal.html'
    truth = [
        ['Title',    1,'title',2, False, 0,  source, 'docid'],
        ['Big title',2,'h1',   3, False, 0,  source, 'docid'],
        ['This is',  3, 'p',   3, False, 0,  source, 'docid'],
        ['some',     3, 'b',   4, True,  8,  source, 'docid'],
        ['content',  3, 'p',   3, True,  12, source, 'docid'],
        ['bye',      4, 'div', 2, False, 0,  source, 'docid']
    ]
    res = []
    def callback(content, block_id, html_tag, **kargs):
        res.append([content,block_id,html_tag,
            kargs['dom_level'],kargs['formatting'],
            kargs['rel_pos'],kargs['path'],kargs['docid']])
    parser.parseHTML(source, docid='docid', callback=callback)
    assert res == truth
