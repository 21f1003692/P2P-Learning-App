# P2P-Learning-App
Peer to Peer Learning App

## Usage

### virtual environment

* python3 -m pip install virtualenv 
* python3 -m virtualenv venv   
* source venv/bin/activate

### run app

* pip install -r requirements.txt
* sqlite3 user.db
* flask db init
* flask db migrate -m "create tables"
* flask db upgrade
#### Main App(User Service)
> flask run