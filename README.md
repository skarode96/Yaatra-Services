# yaatra-services

# ![logo](https://trello-attachments.s3.amazonaws.com/5e9b3762dfe630697c136b9c/5ea33c100871825f327b199c/af631dde2a10ac5a1b091efc3261a878/yaatra.png)

# [![CircleCI](https://circleci.com/gh/skarode96/yaatra-services/tree/master.svg?style=svg)](https://circleci.com/gh/skarode96/Yaatra-Services/tree/master)

### Python Service installation guide

#### 1. Installing all dependencies
`pip install -r requirements.txt`

#### 2. Starting the server
`python manage.py runserver`

#### 3. Running the tests
`coverage run  manage.py test`

`coverage report -m`

`coverage html`

### Postgres setup

#### 1. Download Dbeaver and create database 'yaatra'

#### 2. Start Postgres and run the following commands.

`psql postgres`

#### 3. Create user 'ase' and grant privileges.

`create user ase with password 'ase';`

`alter role ase set client_encoding to 'utf8';`

`alter role ase set default_transaction_isolation to 'read committed';`

`create database yaatra`
 
`grant all privileges on database yaatra to ase`

#### 4. List all databases

`\l` 

`\c yaatra` 

#### 5. In the project folder run the following command

`python manage.py makemigrations`

`python manage.py migrate`
