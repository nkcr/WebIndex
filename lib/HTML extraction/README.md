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
import extractor as parser

result = {}
result = parser.parseHTML('file.html')
# result => {1: 'block1', 2: 'block2', ...}
```

It is possible to give as second argument a function that will be called for
each HTML tag parsed, as the following:

```
callback(content, block_id, html_tag, dom_level, is_formatting)
```

The `dom_level` starts at 1 in the body and is incremented for each level.  
The `is_formatting` indicates that the content is part of an already existing
block. This happens in formatting blocks.

## Test

To launch tests :

```bash
$ py.test test_extractor.py
```

## Dependencies

* python3
* lxml
* py.test
