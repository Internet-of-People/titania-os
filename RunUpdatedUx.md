# ON rpi
## reset the running backend
```bash
sudo pip install flask
systemctl stop vuedj
cd /srv
rm -f vuedj
```

## pull the repo - use your credentials
```bash
git clone https://gitlab.libertaria.community/titania/ux-titania.git
```

## copy the dist folder for front end and vuedj for backend
```bash
cd /srv
cp -r ux-titania/vuedj .
cp -r ux-titania/dist vuedj/
docker stop nginx
docker rm nginx
docker run --name nginx -p 80:80 -p 443:443  -v /srv/vuedj/dist:/usr/html libertaria/nginx:armv7
```

## start monit and backend
```bash
cd /srv/vuedj
python monit_dashboard.py &
python manage.py migrate
python manage.py runserver 0.0.0.0:8000 &
```

