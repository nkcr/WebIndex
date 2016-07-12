# Kocher Noémien july 2016 - HEIA-FR
#
# This script launch all the libs' tests.
# run with `./run_all_tests`. You might need
# to do before `chmod +x run_all_tests`.

# block extraction
cd "lib/Blockextraction"
py.test test_extractor.py -vv
cd "../.."
# HTML extraction
cd "lib/HTMLextraction"
py.test test_extractor.py -vv
cd "../.."
# Indexengine
cd "lib/Indexengine"
py.test test_indexengine.py -vv
cd "../.."
