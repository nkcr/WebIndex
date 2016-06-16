# HTML extractor

## Feature

Extract an HTML file to blocks corresponding to HTML blocks. Formatting blocks
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

## Usage

```python
import extractor as parser

result = {}
result = parser.parseHTML('file.html')
# result => {1: 'block1', 2: 'block2', ...}
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
