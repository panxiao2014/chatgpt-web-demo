This project utilize [flask-volt-dashboard](https://github.com/app-generator/flask-volt-dashboard) which supports running application in docker or on the host. By furtherly following below steps, it can achieve:
- Both docker and host running methods share the same database file
- Source code change will take effect immediately for both running methods

### 1. create a virtual env and install all neccessary libs:
   - virtualenv flask
   - source flask/bin/activate
   - pip3 install -r requirements.txt


### 2. upload openai api key

Put the key string to file configs/openai_api_key.txt

### 3. go to project folder, use following command to init and create database file:
```bash
flask db init
flask db migrate
flask db upgrade
```

### 4. move the created database file outside the project folder:
```
mv apps/db.sqlite3 /opt/sqlite/flask/
```

### 5. in dockerfile, since we already created the database, remove flask db related commands

### 6. in dockerfile, add following command:
```bash
WORKDIR /code
```

### 7. in docker-compose.yml, mount two directoies:
```bash
volumes:
    - .:/code
    - /volume1/dev/sqlite/flask:/volume1/dev/sqlite/flask
```

The first mounted path is to mount the project folder to container working directory /code. So any code change in source files will take effect with docker running;
The second mounted path is to mount the database file directory to container

### 8. in *apps/__init__.py* where database path is defined, change url to the mounted database directory:
```
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI = 'sqlite:////volume1/dev/sqlite/flask/db.sqlite3'
```
