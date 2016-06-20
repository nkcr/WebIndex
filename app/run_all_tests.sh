# block extraction
cd "lib/Blockextraction"
py.test test_extractor.py
cd "../.."
# HTML extraction
cd "lib/HTMLextraction"
py.test test_extractor.py
cd "../.."
# Indexengine
cd "lib/Indexengine"
py.test test_indexengine.py
cd "../.."
