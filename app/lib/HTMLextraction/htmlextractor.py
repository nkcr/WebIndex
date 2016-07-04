'''Parse an HTML file to blocks.

This module gives the ability to get a hash of blocks from an HTML file. Blocks
corresponds to HTML blocks but does not include formatting blocks.

Example:

    <p>Hello</p>
    <p>there</p>
    => {1: 'hello', 2: 'there'}

    <p>Hello <b>there</b></p> are you <i>ready</i>?
    => {1: 'Hello there', 2: 'are you ready ?'}

Module usage:
    parseHTML(source, callback=None)

    Parameters:
        source (string): Path of the HTML file.
        docid (string): The identifier of the document
        callback (func): An optional function that is called when an HTML tag is
            parsed. Func takes as Parameters:
                func(content, block_id, html_tag, **kargs)
                kargs:
                    dom_level (int): Indicates the dom level. Body is at 1.
                    formatting (bool): Indicates that the content is included
                        in an already existing block. This happens in formatting
                        blocks.
                    rel_pos (int): Indicates the position relative to the block.
                    path (string): The path given to parse the file.
                    docid (string): The document id

Author: Noémien Kocher
Licence: MIT
Date: june 2016
'''

from lxml import etree
import random
import os

__formatting_tags = ['b', 'em', 'i', 'a']
'''List of tags that won't be considered as HTML blocks.
'''

def __gettext(el):
    '''Retrieve the text of an lxml element. If None return empty string.
    '''
    if(el.text and el.text.strip()):
        return el.text.strip()
    return ''

def __gettail(el):
    '''Retrieve the tail of an lxml element. If None return empty string.
    '''
    if(el.tail and el.tail.strip()):
        return el.tail.strip()
    return ''

def __store_content(res,content,i):
    '''Clean the content and store it in the hash containing blocks.
    '''
    content = ' '.join(content.split())
    if(content is not ''):
        i += 1
        res[str(i)] = content
    return i

def __clean_space(content):
    return ' '.join(content.split())

def __crawl(elements, i, res, acc, parent_tag,
            dom_level, callback, formatting=False):
    '''Recursively parse each element as block.

    Parameters:
        elements (lxml.etree._Element): The current element.
        i   (int): The current blockId.
        res (dict): The hash containing blocks.
        acc (string): The current text that hasn't been stored yet.
        parent_tag (strin): The parent tag as a string
        dom_level (int): The current dom_level. Body is at level 1
        callback (func): A function that is called for each html tag and takes
            as params: func(content, block_id, html_tag, **kargs)
        formattting (bool): Indicates if it parses formatting blocks.

    Returns:
        acc (string): It not empty, the last content that has to be strored.
        i (int): The last index.
        it (bool): Indicates if it has iterate over element at least once.
    '''
    it = False
    dom_level += 1
    for el in elements:
        it = True
        # This is a formatting block
        # Will only accumulate the content
        if(formatting or el.tag in __formatting_tags):
            a = __gettext(el)
            if(a is not ''):
                callback(a,str(i+1),el.tag,
                dom_level=dom_level, formatting=True, rel_pos=len(__clean_space(acc)))
            (b,i,ite) = __crawl(el,i,res,'',el.tag,dom_level,callback,formatting=True)
            c = __gettail(el)
            acc += ' ' + a + ' ' + b
            if(c is not ''):
                callback(c,str(i+1),parent_tag,
                dom_level=dom_level-1, formatting=True, rel_pos=len(__clean_space(acc)))
                acc += ' ' + c

        # Got a block tag
        else:
            # Because we are in a new block,
            # we save the current accumulator
            if(acc is not ''):
                i = __store_content(res,acc,i)
                acc = ''
            # Push the content and crawl children
            a = __gettext(el)
            if(a is not ''):
                callback(a,str(i+1),el.tag,
                    dom_level=dom_level,formatting=False, rel_pos=0)
            acc += ' ' + a
            (b,i,ite) = __crawl(el,i,res,acc,el.tag,dom_level,callback)
            # It there is no children we need to
            # manually save the block
            if(not ite):
                i = __store_content(res,acc,i)
                acc = ''
            # Push content from the children, which could
            # be the tail of formatting content
            else:
                i = __store_content(res,b,i)
            c = __gettail(el)
            if(c is not ''):
                callback(c,str(i+1),parent_tag,
                    dom_level=dom_level-1, formatting=False, rel_pos=0)
            acc = c

    return (acc,i,it)

def parseHTML(source, docid=None, callback=None):
    '''Parses an HTML file to blocks.

    Parameters:
        source (string): The path of the HTML file.
        docid (string): The identifier of the document
        callback (func): An optional function that is called when an HTML tag is
            parsed. Func takes as Parameters:
                func(content, block_id, html_tag, **kargs)
                kargs:
                    dom_level (int): Indicates the dom level. Body is at 1.
                    formatting (bool): Indicates that the content is included
                        in an already existing block. This happens in formatting
                        blocks.
                    rel_pos (int): Indicates the position relative to the block.
                    path (string): The path given to parse the file.
                    docid (string): The document id

    Returns:
        res (dict): Hash containing HTML blocks
    '''
    res = {}
    if os.stat(source).st_size == 0:
        return res
    parser = etree.HTMLParser(encoding='UTF-8')
    context = etree.parse(source, parser)
    def __callback(content,block_id,html_tag,**kargs):
        if(callback is not None):
            callback(content,block_id,html_tag,path=source,docid=docid,**kargs)

    __crawl(context.getroot().iterchildren(), 0, res, '', '', 0, __callback)
    return res
