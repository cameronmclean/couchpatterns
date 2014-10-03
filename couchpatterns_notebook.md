couchpatterns notebook
======================

###### 20141003
OK - starting new project
another take on pattern strucutre and website - using couchdb, django/python.

used hombew to install and upgrade couchdb

'''
brew upgrade couchdb
'''

installed couchdb 1.6.0

Next - created conda env called _couch_ so we can have a seperate python env for working with couch and new website.

to create the env -

'''
conda create -n couch python=2.7 anaconda
'''

activate/load the env by 

'''
source activate couch
'''

then installed couchdbkit

'''
pip install couchdbkit
'''

'''
pip install django
'''
(get latest version of django 1.7)


created new django project called patternsite

'''
$django-admin.py startproject patternsite
'''

found https://pypi.python.org/pypi/django_couchdb_utils
to enable the use of couchdb with the djano sessions, auth etc
installed by

```
$pip install django_couchdb_utils
```

Using MySQL for django middleware helpers such as auth, sessions etc
needed to 

```
$pip install mysql-python
```

and add `/Applications/mampstack-5.4.26-2/mysql/bin/` to the path in `~/.bash_profile`

created new db in mySQL called couchpatterns `CREATE DATABASE couchpatterns`

then ran

```
$python manage.py migrate
```

to set up all the support tables in mySQL for django middleware.

> all seems to work.

created django app called comfyapp
`$python manage.py startapp comfyapp`

next added support for coucdb by modifying settings.py to inlcude 
```
INSTALLED_APPS = (
    'couchdbkit.ext.django',
    'comfyapp',
    ...
 ```

 and 

 ```
COUCHDB_DATABASES = (
     ('comfyapp’, 'http://127.0.0.1:5984/patterns’),
 )
 ```
