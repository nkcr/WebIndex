import lib.HTMLextraction.htmlextractor as parser
import lib.Blockextraction.blockextractor as blockextractor
import lib.Indexengine.indexengine as iengine
import uuid
import csv
import glob
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
        self.repo[docid] = [ path[7:], sqrt(float(self.engine.normssq[docid])), blocks ]

    def update(self, quantity=10):
        '''Compute the tf-idf and update word ranks. Return the n best words.
        '''
        iengine.settfidf2(self.repo,self.getii())
        iengine.setwrank(self.engine.ii)
        best = iengine.mostranked(quantity,self.getii())
        return best

    def mostranked(self, quantity=10):
        keys = self.update(quantity)
        return iengine.getcontext(self.repo, self.getii(), keys)

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
        iengine.savejson('data/ii.txt', self.getii())

    def saverepo(self):
        iengine.savejson('data/repo.txt', self.repo)

    def savestats(self, path, quantity=100):
        iengine.settfidf2(self.repo,self.getii())
        iengine.setwrank(self.engine.ii)
        keys = iengine.mostranked(quantity,self.getii())
        with open(path, 'w') as csvfile:
            spamwriter = csv.writer(csvfile)
            for k in keys:
                spamwriter.writerow([k,round(self.getii()[k][0],2)])

# webindex = Webindex()
# files = glob.glob('documents/TIF_FR/*.html')
# for file in files:
#     webindex.handlefile(file)
# webindex.savestats('test.csv')
