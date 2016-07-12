# WebIndex
WebIndex is a bachelor project that aims to provide an automatic way to generate
a keywords index based on a collection of web pages. The solution should give to
users a clever representation of the most important subjects on the web pages
and a way to browse them easily.

# Functionalities

* Submit a folder containing HTML pages and generate an index
* Display most important keywords based on an adapted tf-idf algorithm
* Change the number of keywords to display
* Save and read back the generated index
* Change the rank of a word so as to make it less or more important
* Perform a search among all words and change its rank

# Folder structure of the repository

```
└── app             # Web server
    ├── data        # Exported data structures
    ├── lib         # Modules
    ├── static      # Static web assets
    │   └── uploads # Uploaded files
    ├── templates   # HTML view file
    ├── validation  # Algorithms evaluations
    └── venv        # Pyhton virtualenv
```

# How to run the webserver

Go to `/app` run `. venv/bin/activate`. Then do `export FLASK_APP=webstart.py` and `flask run`.

If the server needs to be visible outside localhost, run with `flask run --host=0.0.0.0`. To have the debug mode, do `export FLASK_DEBUG=1`.

You might need to install dependencies, see the README at `/app`.
