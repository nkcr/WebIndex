import HTMLextraction.htmlextractor as parser
import Blockextraction.blockextractor as blockextractor
import Indexengine.indexengine as iengine
import uuid
from math import sqrt

engine = blockextractor.BlockExtractor()

repo = {}

def handlefile(path):
    docid = path + '-' + str(uuid.uuid1())
    blocks = parser.parseHTML(path, docid=docid, callback=engine.handle_block)
    repo[docid] = [ 'url', sqrt(float(engine.normssq[docid])), blocks ]

def test():
    handlefile('HTMLextraction/test_files/simple.html')
    handlefile('HTMLextraction/test_files/full_content.html')
    iengine.settfidf(repo,engine.ii)
    iengine.setwrank(engine.ii)
    best = iengine.mostranked(4,engine.ii)
    print(best)
    print(repo)
    print(engine.ii)

def getii():
    return engine.ii

test()
