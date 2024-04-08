# TengiNews Clone


### Development Environment


#### Installation (Linux)


```bash
git clone git@github.com:TemirlannK2004/Tengri-News-Clone.git

cd Tengri-News-Clone

python3 -m venv venv

source venv/bin/activate

(venv)$ pip install -r requirements.txt
```

#### Configuration
Before applying migrations, creating superusers or running the server, a PostgreSQL database must be created.

```sh
touch .env
```

#.env
```
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
Before proceeding, make sure you have Docker installed. Next enter the command
```bash
  docker-compose up --build
```

After successfully building and running docker containers, enter this commands
```bash
docker-compose exec web bash
python manage.py migrate
python manage.py createsuperuser
```