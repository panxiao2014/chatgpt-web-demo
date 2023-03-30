This project utilize [flask-volt-dashboard](https://github.com/app-generator/flask-volt-dashboard) which supports running application in docker or on the host. By furtherly following below steps, it can achieve:
- Both docker and host running method share the same database file
- Source code change will take effect immediately for both running method

### 1. create a virtual env and install all neccessary libs:
   - virtualenv flask
   - source flask/bin/activate
   - pip3 install -r requirements.txt

### 2. go to project folder, use following command to init and create database file:
```bash
flask db init
flask db migrate
flask db upgrade
```

### 3. move the created database file outside the project folder:
   . mv apps/db.sqlite3 /opt/sqlite/flask/

### 4. in dockerfile, since we already created the database, remove flask db related commands

###5. in dockerfile, and following command:
```bash
WORKDIR /code
```

### 6. in docker-compose.yml, mount two directoies:
```bash
volumes:
    - .:/code
    - /opt/sqlite/flask:/opt/sqlite/flask
```

The first mounted path is to mount the project folder to container working directory /code. So any code change in source files will take effect with docker running;
The second mounted path is to mount the database file directory to container

### 7. in source code where database path is defined (config.py), change url to the mounted database directory:
    . SQLALCHEMY_DATABASE_URI = 'sqlite:////sqlite/db.sqlite3'


### To start docker:
```bash
cd /volume1/dev/code/flask-volt-dashboard
docker-compose up
```

### To start app on host, first activate the python virtual env and then start app by specifying port and address:
```bash
source /volume1/dev/virtualenv/flask/bin/activate
cd /volume1/dev/code/flask-volt-dashboard
flask run -p 5085 -h 192.168.0.114
```
