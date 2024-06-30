# Bible Concord

Enable analyzing on bible text

### Rre Requests
- python 3.11.4
- mysql (user: `root` password: `qazwsxedc`)
- node 20.11.0


### Set Environment

Initialize db
```sh
mysql -h localhost -P 3306 -u root --password=qazwsxedc -e'CREATE DATABASE `bible-concord`;'
```

Install server dependencies + create tables
```sh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt -r requirements.test.txt
alembic upgrade head
```

Setup client
```sh
cd client
npm install
```

### Running Server & Client:

```sh
python -m venv venv
python app.py
cd client
npm start
```

Now you can access app on http://localhost:3000


## checks before pushing commits to remote repository

```sh
pre-commit run --all-files
```
