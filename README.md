# Tele-Marketing
---
### installation for Mac
Install Homebrew
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
Install Homebrew Packages
```
$ brew install python@3.8
$ brew install libpython
$ brew install mysql
$ brew install gdal
```
Change Python version on Mac
```
$ ls -l /usr/local/bin/python*
$ ln -s -f /usr/local/bin/python3.8 /usr/local/bin/python
```

Install Python Packages
```
$ bash install.mac.sh
```
### Run Server
```
$ . ../venv_telem/bin/activate
$ python manage.py runserver 8000
```