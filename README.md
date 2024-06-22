# Bible Concord

Enable analyzing on bible text

### Rre Requests
- python 3.11.4
- mysql (user: `root` password: `BC12345`)



### Set Environment

Initialize db
```sh
mysql -h localhost -P 3306 -u root --password=BC12345 -e'CREATE DATABASE `bible-concord`;'
```

Install dependencies + create tables
```sh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt -r requirements.test.txt
alembic upgrade head
```

### Running:

```sh
python -m venv venv
python app.py
```


## checks before pushing commits to remote repository

```sh
pre-commit run --all-files
```
