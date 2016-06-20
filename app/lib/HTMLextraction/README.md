# HTML extractor

## Features

Extracts an HTML file to blocks corresponding to HTML blocks. Formatting blocks
are not considered as block. For example :

```html
<p>Hello</p>
<p>Folks are you <b>ready</b>?</p>
Always!
```

gives :

```python
{1: 'Hello', 2: 'Folks are you ready ?', 3: 'Always!'}
```

Iteration is guaranteed to be sequential in Depth-first search - in order.

## Usage

```python
import htmlextractor as parser

result = {}
result = parser.parseHTML('file.html')
# result => {1: 'block1', 2: 'block2', ...}
```

It is possible to give as optional arguments the docId and a function that will
be called for each HTML tag parsed, as the following:

```python
callback(content, block_id, html_tag, **kargs)
```

`kargs` contains the following optional parameters:
* dom_level (int): Indicates the dom level. Body is at 1.
* formatting (bool): Indicates that the content is included
        in an already existing block. This happens in formatting
        blocks.
* rel_pos (int): Indicates the position relative to the block.
* path (string): The path given to parse the file.

Example with a docId and a callback:

```python
import htmlextractor as parser

def callback(content, block_id, html_tag, **kargs):
  ...

result = {}
result = parser.parseHTML('file.html', docid='id' callback=callback)
```

## Test

To launch tests :

```bash
$ py.test test_extractor.py
```

## Dependencies

* python3
* lxml
* py.test
