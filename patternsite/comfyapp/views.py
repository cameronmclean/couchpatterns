from django.shortcuts import render, redirect
from django.http import Http404
import re
from comfyapp import slug
from django.contrib.auth.decorators import login_required

############################################
# settting up connections and couchdb here - maybe not the best place but trying for now...
############################################
from couchdb import Server
from couchdb import ResourceNotFound

SERVER = Server("http://127.0.0.1:5984/")
if (len(SERVER) == 0):
	SERVER.create('patterns')



# Create your views here.

def home(request):
	return render(request, 'index.html')

def nope(request):
	return render(request, 'nope.html')

def logout_view(request):
	logout(request)
	return redirect ("/")

@login_required
def add(request):
	
	#check to see if logged in/authenticated..
	#put code here
	
	#set patterns as the document database 
	patternsdb = SERVER['patterns']

	#grab the form data that is POSTed, store it in a dict, then save the dict
	#to the db, with a document id dlugged from the pattern name.
	
	if request.method == "POST":
		name = request.POST['name']
		authors = request.POST['authors'].split(", ")
		context = request.POST['context']
		problem = request.POST['problem']
		forces = request.POST
		
		# consolidate all the posted data into a dict
		pattern_to_save = {"name":name, "authors":authors, "context":context, "problem":problem}
		#create a human friendly doc name + URL) to save the pattern
		#slug() converts spaces to - , transform to lowercase, strip all non-alphanumeric
		doc_name = slug.slug(name)
		

		# attempt to save the document
		try: 
			patternsdb[doc_name] = pattern_to_save
		
			return redirect ('/')
		#if it fails, it might be because a pattern with this name already exists
		# for now, redirect to generic error page with suggestions
		#find a better way of handling errors in the future though.
		except:

			return redirect ("/nope")
	
	return render(request, 'add.html')
	
	#get a list of all pattern doc IDs in the db 
#	patterndoc_ids = []
#	for item in patternsdb:
#		patterndoc_ids.append(item)
	#store all the patterns docs in a list, to be passed to the template
#	patterns = []
#	for ids in patterndoc_ids:
#		patterns.append(patternsdb[ids])
	
	#patterndoc = patternsdb['40bab7710410edf83d42f170cb000bcf']
	#try:
	#	doc = patternsdb['_id']
	#except ResourceNotFound:
	#	raise Http404
	
	#print patternsdb
	#for item in patternsdb:
#		print item
	#print patterndoc

	#pattern = patterns['name']
	#except ResourceNotFound:
	#	raise Http404


	return render(request, 'add.html', {'patterns':patterns})