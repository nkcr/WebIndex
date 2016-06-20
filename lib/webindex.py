import HTMLextraction.htmlextractor as parser
import Blockextraction.blockextractor as blockextractor

engine = blockextractor.BlockExtractor()

def handlefile(path):
    blocks = parser.parseHTML(path, callback=engine.handle_block)

def test():
    handlefile('HTMLextraction/test_files/simple.html')

def getii():
    return engine.ii
