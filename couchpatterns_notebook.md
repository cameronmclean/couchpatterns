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

OK!

NOTE - needed to remove the line
`from django.db.models.options import get_verbose_name`
from /Users/cameronmclean/anaconda/envs/couch/lib/python2.7/site-packages/couchdbkit/ext/django/schema.py
and add 

```
# Calculate the verbose_name by converting from InitialCaps to "lowercase with spaces".
get_verbose_name = lambda class_name: re.sub('(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))', ' \\1', class_name).lower().strip()
```
in order to make couchdbkit work with Django 1.7

#####201401006

OK - maybe not couchdbkit django extension - bit hard to figure out exactly what is going on.
Can try own manual management using python package couchdb
http://pythonhosted.org//CouchDB/index.html
'pip install couchdb'

also, to the couchdb local.ini (/usr/local/etc/couchdb/)
added 

```
[query_servers]
python = /Users/cameronmclean/anaconda/envs/couch/bin/couchpy
```

this way we can use python to write views and map/reduce fucntions. seems to work. cool!

Also, downloaded website template from HTML5up http://html5up.net/
copied index.html to django app /templates dir, and placed remaining folders in /static.
needed to modify index.html and style.css to refelct the paths for static files had chaged, also modified style.css to replace stock images with sciency ones.

licenses.txt in /static/images captures the CC licences - but need to put these on the webpage (along with HTML5up attribution).

Wrote a urls.py and basic views.py to hook up 'home' with the new index.html.

Looks good!


######20141008
OK.
So got simple forms working via the "add" view in django to create a new document in the couchdb database.

Rather than use the UUID that couchdb provides as the _id, i created a slug from the pattern name
to render doc id as lowercase, alphanumberic, spaces converted to dashes .
This makes for nice URI/Ls for repurposing data directly from couchs RESTfulAPI.
i.e pattern name "Photons Alive!" is id and accessed by
http://127.0.0.1:5984/patterns/photons-alive

slug.py does the job using regex and python string methods

```python
import re

def slug(string_to_slug):
	words = str(string_to_slug)
	lower = words.lower().replace(' ', '-')
	slugged = re.sub(r'[^a-z0-9-]+', '', lower)
	return slugged
```

next is to define all the form fields, and hook them up to request.POST 
####tricky as we want to 1) allow for multiple authors, 2)multiple forces (i,e add remove dynamic) and define a custom fields..
//perhaps leave out the custom fields for now - user would need to know if its a string, int, list, dict, attachment etc...

#### for later work - editing patterns - would be good to dynamically grab all the keys/values so that as any pattern or document evolves, we dont have to change the edit view. 
