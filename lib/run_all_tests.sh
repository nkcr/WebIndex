# block extraction
py.test Blockextraction/test_extractor.py
# HTML extraction
cd "HTMLextraction"
py.test test_extractor.py
cd ".."
# Indexengine
py.test Indexengine/test_indexengine.py
