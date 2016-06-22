# Block extractor

## Features

Provides function to manipulate an inverted index.

* Compute tf-idf for each occurence of a word in a document
* Update the rank of each word
* Retrieve the n best words
* Save an inverted index to a json file
* Save the repository as a json file

## Usage

```python
import indexengine as iengine

iengine.settfid(repo, ii)
iengine.setwrank(ii)
keys = iengine.mostranked
iengine.saveii(path, ii)
iengine.saverepo(path, repo)
```


## Test

To launch tests :

```bash
$ py.test test_indexengine.py
```

## Dependencies

* python3
* py.test
