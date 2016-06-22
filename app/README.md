# How to run

Run `. venv/bin/activate`. Then do `export FLASK_APP=webstart.py` and `flask run`.

If the server needs to be visible outside localhost, run with `flask run --host=0.0.0.0`. To have the debug mode, do `export FLASK_DEBUG=1`.

# Test

Run all the tests with:

```
./run_all_tests.sh
```

# Dependencies

* virtualenv
* lxml
* python3
* Flask
* nltk
