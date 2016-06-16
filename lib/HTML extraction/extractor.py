from lxml import etree
import random
import os

source = 'document.html'

def __gettext(el):
    if(el.text and el.text.strip()):
        return el.text.strip()
    return None

def __gettail(el):
    if(el.tail and el.tail.strip()):
        return el.tail.strip()
    return None

__formatting_tags = ['b', 'em', 'i']

def __xstr(s):
    return '' if s is None else str(s)
def __crawl(elements, i, res, formatting=False):
    topel = ''
    for el in elements:
        # if(not formatting):
        #     topel = ''
        if(formatting and el.tag in __formatting_tags):
            a = __gettext(el)
            (b, i) = __crawl(el.iterchildren(), i, res, formatting=True)
            c = __gettail(el)
            topel += ' ' + __xstr(a) + ' ' + __xstr(b) + ' ' + __xstr(c)
        elif(el.tag not in __formatting_tags and el.getchildren() and el.getchildren()[0].tag in __formatting_tags):
            a = __gettext(el)
            (b, i) = __crawl(el.iterchildren(), i, res, formatting=True)
            c = __xstr(__gettail(el))
            topel += ' ' + __xstr(a) + ' ' + __xstr(b)
            i += 1
            res[i] = ' '.join(topel.split())
            topel = ''
            if(c):
                i += 1
                res[i] = c
        else:
            if(el.tag in __formatting_tags):
                tmp = ''
                if(__gettext(el)):
                    tmp = __gettext(el)
                (b, i) = __crawl(el.iterchildren(), i, res, formatting=True)
                tmp += ' ' + b
                if(__gettail(el)):
                    tmp += ' ' + __gettail(el)
                if(el.getnext() is not None and el.getnext().tag in __formatting_tags):
                    topel += ' ' + tmp
                elif(tmp is not ''):
                    i += 1
                    res[i] = ' '.join((topel + ' ' + tmp).split())
                    topel = ''
            else:
                if(__gettext(el)):
                    i += 1
                    res[i] = topel + __gettext(el)
                (_, i) = __crawl(el.iterchildren(), i, res)
                if(__gettail(el)):
                    if(el.getnext() is not None and el.getnext().tag in __formatting_tags):
                        topel += ' ' + __gettail(el)
                    else:
                        i += 1
                        res[i] =  __gettail(el)
    return (topel, i)

def parseHTML(source):
    res = {}
    if os.stat(source).st_size == 0:
        return res
    context = etree.parse(source)
    __crawl(context.getroot().iterchildren(), 0, res)
    return res
