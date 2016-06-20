# Block extractor

## Features

Tokenizes a string block to an inverted index. For example, given the following
parameters:

```python
handle_block("Lorem-ipsum dolor", 12, 'p', docid='docid', rel_pos=10)
```

It will output an inverted index in the form:

```python
{
  wordId: [
    rank, {
      docId: [
        nbHit, rank,[
          [blockId, position, domLevel],
          ...
        ]
      ],
      ...
    }
  ],
  ...
}
```

## Usage

```python
import blockextractor as parser

engine = parser.BlockExtractor()
engine.handle_block(content, block_id, html_tag, **kargs)
# kargs are {block_id, rel_pos}
inverted_index = engine.ii
```

Parameters are the same that are required in the 'htmlextractor.py' module.

## Test

To launch tests :

```bash
$ py.test test_extractor.py
```

## Dependencies

* python3
* py.test
