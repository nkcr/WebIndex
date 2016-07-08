# Install

```
sudo apt-get install libxml2 libxml2-dev libxslt1-dev
pip3 install -r requirements.txt
```

# Run the webserver

Run `. venv/bin/activate`. Then do `export FLASK_APP=webstart.py` and `flask run`.

If the server needs to be visible outside localhost, run with `flask run --host=0.0.0.0`. To have the debug mode, do `export FLASK_DEBUG=1`.

To leave the virtualenv type :

```
deactivate
```

# Test

Run all the tests with:

```
. venv/bin/activate
./run_all_tests.sh
```

# Dependencies

* virtualenv
* lxml
* python3
* Flask
* nltk
