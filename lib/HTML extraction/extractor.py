from lxml import etree
import random
import os

def __gettext(el):
    if(el.text and el.text.strip()):
        return el.text.strip()
    return ''

def __gettail(el):
    if(el.tail and el.tail.strip()):
        return el.tail.strip()
    return ''

__formatting_tags = ['b', 'em', 'i']

def __store_content(res,content,i):
    content = ' '.join(content.split())
    if(content is not ''):
        i += 1
        res[i] = content
    return i

def __crawl(elements, i, res, acc, formatting=False):
    it = False
    for el in elements:
        it = True

        # This is a formatting block
        # Will only accumulate the content
        if(formatting or el.tag in __formatting_tags):
            a = __gettext(el)
            (b,i,ite) = __crawl(el,i,res,'',formatting=True)
            c = __gettail(el)
            acc += ' ' + a + ' ' + b + ' ' + c

        # Got a block tag
        else:
            # Because we are in a new block,
            # we save the current accumulator
            if(acc is not ''):
                i = __store_content(res,acc,i)
                acc = ''
            # Push the content and crawl children
            a = __gettext(el)
            acc += ' ' + a
            (b,i,ite) = __crawl(el,i,res,acc)
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
            acc = c

    return (acc,i,it)

def parseHTML(source):
    res = {}
    if os.stat(source).st_size == 0:
        return res
    context = etree.parse(source)
    __crawl(context.getroot().iterchildren(), 0, res, '')
    return res
