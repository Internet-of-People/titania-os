# ux

Configuration and monitoring unit for titania.

## running vuejs frontend

``` bash
cd ux
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

## django rest framework backend

``` bash
source .venv/bin/activate
cd vuedj
python manage.py runserver
python manage.py makemigrations configtitania
# to see the sql query
python manage.py sqlmigrate configtitania 0001
python manage.py migrate
```

## serve build files from vuejs frontend

```bash
docker pull nginx
git clone https://github.com/Internet-of-People/titania-os.git
docker run --name nginx -p 80:80 -p 443:443  -v /home/root/titania-os/ux/dist:/usr/html libertaria/nginx:armv7
```

Then simply open the rpi's ip on your browser.

## Install and Run django backend

``` bash
cd ux/vuedj
python monit_dashboard.py &
python manage.py makemigrations
python manage.py makemigrations configtitania
python manage.py migrate
python manage.py runserver 0.0.0.0:8000 &
```

## Integrated image

``` bash
# configuration interface backend
systemctl restart vuedj
# monitoring service
systemctl restart docker-monitoring
```
