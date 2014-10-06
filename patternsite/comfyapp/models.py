from django.db import models
from couchdbkit.ext.django.schema import *


# Create your models here.

class Pattern(Document):
	title = StringProperty()
	authors = ListProperty()
	context = StringProperty()
	problem = StringProperty()
	forces = DictProperty()
	evidence = ListProperty()
