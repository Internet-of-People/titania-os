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

# rPi
## Run Frontend
```
docker pull nginx
git clone https://gitlab.libertaria.community/titania/ux-titania.git
docker run --name nginx -p 80:80 -p 443:443  -v /home/root/ux-titania/dist:/usr/html libertaria/nginx:armv7
```
Then simply open the rpi's ip on your browser.

## Install and Run django backend
```sudo pip install flask```
``` bash
cd ux-titania/vuedj
python monit_dashboard.py &
python manage.py makemigrations
python manage.py makemigrations configtitania
python manage.py migrate
python manage.py runserver 0.0.0.0:8000 &
```

## Integrated image
``` bash
systemctl restart vuedj 
systemctl restart docker-monitoring 
```

## Add Services
```
git clone ssh://git@gitlab.libertaria.community:2200/titania/sample-dapps-services.git
cd sample-dapps-services
npm init
node app.js
```