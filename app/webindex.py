import lib.HTMLextraction.htmlextractor as parser
import lib.Blockextraction.blockextractor as blockextractor
import lib.Indexengine.indexengine as iengine
import uuid
from math import sqrt

class Webindex:

    def __init__(self):
        self.engine = blockextractor.BlockExtractor()
        self.repo = {}

    def handlefile(self, path):
        '''Parse a file to blocks and tokenize each block filling the inverted index.
        Also updates the repo data structure.
        '''
        docid = path# + '-' + str(uuid.uuid1())
        blocks = parser.parseHTML(path, docid=docid, callback=self.engine.handle_block)
        self.repo[docid] = [ 'url', sqrt(float(self.engine.normssq[docid])), blocks ]

    def update(self, quantity=10):
        '''Compute the tf-idf and update word ranks. Return the n best words.
        '''
        iengine.settfidf(self.repo,self.getii())
        iengine.setwrank(self.engine.ii)
        best = iengine.mostranked(quantity,self.getii())
        return best

    def mostranked(self, quantity=10):
        '''Update and return the n best words with their context.
        '''
        keys = self.update(quantity)
        res = []
        offset = 20
        print('#########')
        print(keys)
        for k in keys:
            for docid, value in self.getii()[k][1].items():
                hit = value[2][0]
                blockid = hit[0]
                position = hit[1]
                starti = position-offset
                if(starti<0):
                    starti = 0
                endi = position+len(k)+offset
                content = self.repo[docid][2][blockid]
                wbefore = content[starti:position]
                if(starti > 0):
                    wbefore = '...' + wbefore
                wafter = content[position+len(k):endi]
                if(endi < len(content)):
                    wafter = wafter + '...'
                res.append([k,self.getii()[k][0],wbefore,wafter])
        return res

    def test(self):
        handlefile('lib/HTMLextraction/test_files/simple.html')
        handlefile('lib/HTMLextraction/test_files/full_content.html')
        iengine.settfidf(self.repo,self.getii())
        iengine.setwrank(engine.ii)
        best = iengine.mostranked(4,self.getii())
        print(best)
        print(self.repo)
        print(self.getii())

    def getii(self):
        return self.engine.ii

    def saveii(self):
        iengine.saveii('ii.txt', self.getii())

    def saverepo(self):
        iengine.saverepo('repo.txt', self.repo)
