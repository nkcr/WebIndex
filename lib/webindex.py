import HTMLextraction.htmlextractor as parser
import Blockextraction.blockextractor as blockextractor

engine = blockextractor.BlockExtractor()

def handlefile(path):
    parser.parseHTML(path, engine.handle_block)

handlefile('HTMLextraction/test_files/simple.html')

print(engine.ii)
