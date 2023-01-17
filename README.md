### TASK 10 - SQL

### Create doker container and configure db

##### Docker pull
```sh
docker pull postgres
```
#####

#### Doker build
```sh
docker-compose build
```
#####


##### Doker run
```sh
docker-compose up
```
#####

#### Check container
```sh
docker ps
```
#####

#####
#### Stop container
```sh
docker stop course
docker stop test
docker stop flask
```
#####

#### Remove container
```sh
docker rm course
docker rm test
docker rm flask
```
#####


#### Install
```sh
 pipenv shell
 pipenv install
```
####


#### Check migrate from .pre-commit-config.yaml
```sh
pre-commit migrate-config
```
####

#### Check isort mypy hooks
```sh
pre-commit run --all-files
```
####

#### Check flake8
```sh
flake8
```
####
#### Set environment variable
```sh
export DB_CONNECTION_STRING="postgresql+psycopg2://user2:Rootmode2@localhost:6432/course"
```
####

#### Initialized the database
```sh
python database_tools_script.py --init_db
```
####

#### Populate database with generated random data 
```sh
python database_tools_script.py --pop_db
```
####

#### Start flask app
````sh
python app.py
````
