#!/bin/bash

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
# brew install python@$PY_VERSION
# brew install libpython
# brew install mysql
# brew install gdal


alias python=python3
alias pip=pip3

if [ ! -d "$VENV_DIR" ]; then
    python -m venv $VENV_DIR
fi

cd $PROJECT

# 進入虛擬環境
. ../$VENV_DIR/bin/activate
# 安裝套件
python -m pip install --upgrade pip wheel
# pip install ConcurrentLogHandler, error in ConcurrentLogHandler setup command: use_2to3 is invalid
pip install setuptools==57.5.0
pip install Django
pip install ConcurrentLogHandler
pip install mysqlclient
pip install uwsgi
pip install celery
pip install boto3
pip install pycryptodome
pip install matplotlib
pip install django-debug-toolbar
pip install django-allauth
pip install rest-framework-pagination
pip install drf-spectacular
pip install django-storages
pip install python-decouple
pip install django-redis
pip install openpyxl
pip install pandas
pip install -r requirements.txt
# ~~~~~~~~~~~~~~結束~~~~~~~~~~~~~~

# 安裝程式
# brew install memcached
# brew install rabbitmq-server
# brew install redis

# 資料表更新 => 開發環境不執行
# python manage.py makemigrations
# python manage.py migrate

# # 第一次 makemigrations 的動作 ！！
# python manage.py makemigrations user
# python manage.py migrate

python manage.py collectstatic --noinput

# 排程更新
# python manage.py crontab remove
# python manage.py crontab add

# 啟動程式
# python manage.py runserver 8000

# GDAL error
# /telem/settings.py 292,293 remove remark