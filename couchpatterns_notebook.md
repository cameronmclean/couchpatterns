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

next is to define all the form fields, and hook them up to request.POST so that the add view takes in and stores all the things we want.
####tricky as we want to 1) allow for multiple authors, 2)multiple forces (i,e add remove dynamic) and define a custom fields..
//perhaps leave out the custom fields for now - user would need to know if its a string, int, list, dict, attachment etc...

#### for later work - editing patterns - would be good to dynamically grab all the keys/values so that as any pattern or document evolves, we dont have to change the edit view. 


######20141013

Ok - remember to `source activate couch` before launching and doing all the things each dev session.

ALSO - remember, at the moment we are running mySQL and couchdb - with the idea fof using mySQL to manage useraccounts, and couch just to store the pattern data.
This is to avoid having to custom make our own sessions and authentication framework.

Makes deployment complex/pain, but radid development possible (for me, with limited backgorund in coding and the web)

installed 
`pip install django-registration-redux`
The registration package compatible with django 1,7
http://stackoverflow.com/questions/23037807/django-registration-compatibility-issue-with-django-1-7?rq=1

then ran `python manage.py migrate` to install teh app and mySQL tables/models

django-registration docs are here
https://django-registration.readthedocs.org/en/latest/quickstart.html

to ursl.py added
`(r'^accounts/', include('registration.backends.default.urls')),`

creates teh following url paths

```
^accounts/ ^activate/complete/$ [name='registration_activation_complete']
^accounts/ ^activate/(?P<activation_key>\w+)/$ [name='registration_activate']
^accounts/ ^register/$ [name='registration_register']
^accounts/ ^register/complete/$ [name='registration_complete']
^accounts/ ^register/closed/$ [name='registration_disallowed']
^accounts/ ^login/$ [name='auth_login']
^accounts/ ^logout/$ [name='auth_logout']
^accounts/ ^password/change/$ [name='auth_password_change']
^accounts/ ^password/change/done/$ [name='auth_password_change_done']
^accounts/ ^password/reset/$ [name='auth_password_reset']
^accounts/ ^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$ [name='auth_password_reset_confirm']
^accounts/ ^password/reset/complete/$ [name='auth_password_reset_complete']
^accounts/ ^password/reset/done/$ [name='auth_password_reset_done'] 
```

Created a template in couchpatterns/patternsite/comfyapp/templates/resgistration/registration_form.html

just uses the {{ form }} context variable and magically addds usernam, email, psw1/2.
Cool.
Hooked up a "submit" button with the post method and the action pointing to the same page.
`<form action="/accounts/register/" method='post'>`
Getting the registration form working on the page was as simple as 
```
<form action="/accounts/register/" method='post'>
			{% csrf_token %}
{{form}}
<br>
<div id="cam">
<input type="submit" value="Submit" />
</div>
</form>
```

(note - submit button wrapped in cam <div> just to center it with css)

After the user hits 'submit', the form data is validated and added to the mySQL db.
the user is emailed an activation key and link.
I dont have an SMTP server set up, so putting 
`EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'`
into settings.py causeses the email to print to console rather than go to the smtp server.
we need to specify a activation\_email.txt and activation\_email_subject.txt for the subject and body of the email that is sent.
This txt/email uses the {{ activation_key }} context variable.

copying the activation url works, and then sends us to the next url/template -
`/templates/registration/activation.complete.html` 
(this changes the db to user=active)

we are next asked to login - this requires a template at
`templates/registration/login.html`
- created this with a simple hand made form

```
<form id="login_form" method="post" action="/accounts/login/">
            {% csrf_token %}
            Username: <input type="text" name="username" value="" size="50" />
            <br />
            Password: <input type="password" name="password" value="" size="50" />
            <br />

            <input type="submit" value="submit" />
        </form>
```
upon submit, this redirects us to accounts/profile - which is not found in urls.py...

added `LOGIN_REDIRECT_URL = '/'` to settings.py - not ideal - better if we can capture the page
user was on before login and return that, but OK for now.

current problem - POSTing a new pattern with the @login_required throws a 

>MultiValueDictKeyError at /add/
>"'context'"

somthing to do with the decorator buggering up getting the 'context' from the POST.
might be because context is a reserved / "context" variable?
try changing context names for pattern form/input/post/couch and see...
NOPE - I was just half way through adding new fields - the view was expecting a POST that contained problem and context, the template form didnt have these yet...
duh!

OK - next to fix html <header> for the correct nav bar, create dyanmic forms, and properly style the page...

#####20141015

OK - so fixed minor issue with login redirects.
Needed to add
`<input name="next" type="hidden" value="{{next}}">`
into the login form, while keeping 
`LOGIN_REDIRECT_URL = '/'` in settings.py

answer was found here
http://stackoverflow.com/questions/16307095/django-registration-login-redirection

Now clicking login picks up the page you are on and passes it as a context variable {{ next }} to the login view for the redirect.

cool bananas. Hopefully this will work later when browsing while not logged in and wanting to edit a pattern > login > display forms for editing.


