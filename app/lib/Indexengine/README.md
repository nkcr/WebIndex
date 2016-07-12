# Block extractor

## Features

Provides function to manipulate an inverted index.

* Compute tf-idf for each occurence of a word in a document `settfidf2`
* Update the rank of each word `setwrank`
* Retrieve the n best words `mostranked`
* Save a data-structure to a json file `savejson`
* Import a data-structure as json file `importjson`
* Get the context of occurrences `getcontext`
* Get all the words `words`

## Usage

```python
import indexengine as iengine

iengine.settfid2(repo, ii)
iengine.setwrank(ii)
keys = iengine.mostranked
iengine.savejson(path, ii)
repo = iengine.importjson(path, repo)
contexts = iengine.getcontext(repo, ii, keys, offset=40)
words = iengine.words(ii)
```


## Test

To launch tests :

```bash
$ py.test test_indexengine.py
```

## Dependencies

* python3
* py.test
