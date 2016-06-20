import lib.HTMLextraction.htmlextractor as parser
import lib.Blockextraction.blockextractor as blockextractor
import lib.Indexengine.indexengine as iengine
import uuid
from math import sqrt

engine = blockextractor.BlockExtractor()

repo = {}

def handlefile(path):
    docid = path + '-' + str(uuid.uuid1())
    blocks = parser.parseHTML(path, docid=docid, callback=engine.handle_block)
    repo[docid] = [ 'url', sqrt(float(engine.normssq[docid])), blocks ]

def update(quantity=10):
    iengine.settfidf(repo,engine.ii)
    iengine.setwrank(engine.ii)
    best = iengine.mostranked(quantity,engine.ii)
    return best

def test():
    handlefile('lib/HTMLextraction/test_files/simple.html')
    handlefile('lib/HTMLextraction/test_files/full_content.html')
    iengine.settfidf(repo,engine.ii)
    iengine.setwrank(engine.ii)
    best = iengine.mostranked(4,engine.ii)
    print(best)
    print(repo)
    print(engine.ii)

def getii():
    return engine.ii

def saveii():
    iengine.saveii('ii.txt', engine.ii)

def saverepo():
    iengine.saverepo('repo.txt', repo)
