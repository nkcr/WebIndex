# WebIndex
Bachelor project

# How to run the webserver

Go to `/app` run `. venv/bin/activate`. Then do `export FLASK_APP=webstart.py` and `flask run`.

If the server needs to be visible outside localhost, run with `flask run --host=0.0.0.0`. To have the debug mode, do `export FLASK_DEBUG=1`.

# Folder structure of the repository

```
└── app             # Web server
    ├── data        # Exported data structure
    ├── lib         # Modules
    ├── static      # Static web assets
    │   └── uploads # Uploaded files
    ├── templates   # HTML view file
    ├── validation  # Algorithms evaluations
    └── venv        # Pyhton virtualenv
```
