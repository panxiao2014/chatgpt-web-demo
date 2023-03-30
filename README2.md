While we can run docker by steps in README.md, it does not support sharing source code on host so when code change could reflect to docker running instance.
It also could not mount local sqlite database file to docker container so user's registration info in docker could be saved to local host. Below is the step to achieve this two needs:

1. create a virtual env and install all neccessary libs:
   . virtualenv flask
   . source flask/bin/activate
   . pip3 install -r requirements.txt

2. go to project folder, init and create database file:
   . flask db init
   . flask db migrate
   . flask db upgrade

3. move the created database file outside the project folder:
   . mv apps/db.sqlite3 /opt/sqlite/flask/

4. in dockerfile, since we already created the database, remove flask db related commands

5. in docker file, and following command:
    . WORKDIR /code

6. in docker-compose.yml, mount two directoies:
        volumes:
      - .:/code
      - /opt/sqlite/flask:/sqlite

   the first mounted path is to mount the project folder to container working directory /code. So any code change in source files will take effect;
   the second mounted path is to mount the database file directory to container

7. in source code where database path is defined (config.py), change url to the mounted database directory:
    . SQLALCHEMY_DATABASE_URI = 'sqlite:////sqlite/db.sqlite3'


To start docker:
cd /volume1/dev/code/flask-volt-dashboard
docker-compose up

To start app on host:
source /volume1/dev/virtualenv/flask/bin/activate
cd /volume1/dev/code/flask-volt-dashboard
flask run -p 5085 -h 192.168.0.114
