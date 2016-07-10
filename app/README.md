# Deploy

## Install dependencies

```
sudo apt-get install python3-pip
pip3 install uwsgi
sudo apt-get install libxml2 libxml2-dev libxslt1-dev
pip3 install -r requirements.txt
```

## NGINX conf

```
location / { try_files $uri @yourapplication; }
location @yourapplication {
    include uwsgi_params;
    uwsgi_pass unix:/tmp/yourapplication.sock;
}
client_max_body_size 10M;
```

## Create upload folder

```
mkdir app/static/uploads
```

## Launch application server

```
uwsgi -s /tmp/uwsgi.sock --manage-script-name --mount /=webstart:app
```

## Change socket permission
```
chmod 777 /tmp/uwsgi.sock
```

# Run the webserver in local

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
