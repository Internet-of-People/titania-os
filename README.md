# ux-titania

> configuration and monitoring ux for titania

## Build Setup

``` bash
# install dependencies
npm install

# serve with hot reload at localhost:8080
npm run dev
```
## Set up compass for parsing css

``` bash
# On Windows:
gem install compass

# On OS X:
sudo gem install compass

cd ux-titania/src/assets/css/sass
compass watch --poll

```
## Backend

``` bash
source .venv/bin/activate
cd vuedj
python manage.py runserver

```

``` bash
python manage.py makemigrations configtitania

# to see the sql query
python manage.py sqlmigrate configtitania 0001


python manage.py migrate
```
