#!/bin/bash

# 更新code
git reset --hard
git pull

# 每個專案須一致的安裝模板
# ~~~~~~~~~~~~~~開始~~~~~~~~~~~~~~
# PROJECT 專案名稱 
PROJECT=telem
# PY_VERSION python版本 
PY_VERSION=3.8

cd ..
VENV_DIR=venv_$PROJECT
VERSION=$(python$PY_VERSION -V 2>&1)

echo $VERSION

# 檢測安裝python
case $VERSION in (*"Python $PY_VERSION"*)
        echo 已安裝python $PY_VERSION
    ;;
(*)
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt install python$PY_VERSION -y
;;esac

# 看需求開啟或關閉註解
sudo apt install python$PY_VERSION-venv -y
sudo apt install libpython$PY_VERSION-dev -y
# sudo apt install python$PY_VERSION-tk -y

if [ ! -d "$VENV_DIR" ]; then
    python$PY_VERSION -m venv $VENV_DIR
fi

cd $PROJECT

# 進入虛擬環境
. ../$VENV_DIR/bin/activate
# 安裝套件
python -m pip install --upgrade pip wheel
# pip install ConcurrentLogHandler, error in ConcurrentLogHandler setup command: use_2to3 is invalid
pip install setuptools==57.5.0
pip install -r requirements.txt
# ~~~~~~~~~~~~~~結束~~~~~~~~~~~~~~

# 設定檔複製 專案上一層的settings裡的資料複製到專案內
cp -r ../settings/. .

mkdir ../data
mkdir ../output_file

sudo mkdir /var/log/$PROJECT
sudo mkdir /var/log/$PROJECT/django
# sudo mkdir /var/log/$PROJECT/celery

# logs data output_file連結
sudo rm -rf $PWD/logs
ln -s /var/log/$PROJECT/django $PWD/logs

sudo rm -rf $PWD/data
ln -s $PWD/../data $PWD/data

sudo rm -rf $PWD/output_file
ln -s $PWD/../output_file $PWD/output_file

# ln virtualenv
sudo rm -rf /var/www/venv_$PROJECT
sudo ln -s $PWD/../venv_$PROJECT /var/www/venv_$PROJECT

# ln workspace
sudo rm -rf /var/www/$PROJECT
sudo ln -s $PWD /var/www/$PROJECT

# ln nginx.conf to nginx
sudo rm /etc/nginx/sites-enabled/$PROJECT.conf
sudo ln -s /var/www/$PROJECT/nginx.conf /etc/nginx/sites-enabled/$PROJECT.conf

# ln worker & beat conf to supervisor
# sudo rm /etc/supervisor/conf.d/$PROJECT.celeryworker-default.conf
# sudo rm /etc/supervisor/conf.d/$PROJECT.celeryworker-schedule.conf
# sudo rm /etc/supervisor/conf.d/$PROJECT.celeryworker-long.conf
# sudo rm /etc/supervisor/conf.d/$PROJECT.celerybeat.conf
# sudo ln -s /var/www/$PROJECT/celeryworker-default.conf /etc/supervisor/conf.d/$PROJECT.celeryworker-default.conf
# sudo ln -s /var/www/$PROJECT/celeryworker-schedule.conf /etc/supervisor/conf.d/$PROJECT.celeryworker-schedule.conf
# sudo ln -s /var/www/$PROJECT/celeryworker-long.conf /etc/supervisor/conf.d/$PROJECT.celeryworker-long.conf
# sudo ln -s /var/www/$PROJECT/celerybeat.conf /etc/supervisor/conf.d/$PROJECT.celerybeat.conf

# ln uwsgi.ini to uwsgi
# create a directory for the vassals
sudo mkdir /etc/uwsgi
sudo mkdir /etc/uwsgi/vassals
# symlink from the default config directory to your config file
sudo rm /etc/uwsgi/vassals/$PROJECT.ini
sudo rm /etc/uwsgi/apps-enabled/$PROJECT.ini
sudo ln -s /var/www/$PROJECT/uwsgi.ini /etc/uwsgi/vassals/$PROJECT.ini
sudo ln -s /var/www/$PROJECT/uwsgi.ini /etc/uwsgi/apps-enabled/$PROJECT.ini

# chown all to current user
sudo chown -R $USER:$USER $PWD
sudo chown -R $USER:$USER $PWD/../venv_$PROJECT
sudo chown -R $USER:$USER /var/www/venv_$PROJECT
sudo chown -R $USER:$USER /var/www/$PROJECT
sudo chown -R $USER:$USER /etc/uwsgi/vassals
sudo chown -R $USER:$USER /var/log/$PROJECT

# django migration
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput

# request supervisor to bring up celery
# sudo supervisorctl update all
# sudo supervisorctl restart $PROJECT.celeryworker-default
# sudo supervisorctl restart $PROJECT.celeryworker-schedule
# sudo supervisorctl restart $PROJECT.celeryworker-long
# sudo supervisorctl restart $PROJECT.celerybeat

# restart nginx
sudo /etc/init.d/nginx restart

# reboot uwsgi by touch
touch uwsgi.ini
