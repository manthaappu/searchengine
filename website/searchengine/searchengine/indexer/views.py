# Create your views here.

from django.http import HttpResponse
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, logout
from django.contrib.auth.models import User

from searchengine.indexer.models import *
from searchengine.search.models import *



import os,sys
import ntpath
import re
import glob
import pickle
from math import sqrt,log
from stemming.porter2 import stem
from bs4 import BeautifulSoup
from django.utils.encoding import smart_str




def Index(doc_name):


	soup = BeautifulSoup(open(doc_name))
	doc_text = smart_str(soup.body.text) # parse body only
	doc_text = (doc_text + ' ' + smart_str(soup.title.text)).lower()
	doc_text = re.sub(r'[^0-9a-z]',' ',doc_text)
	doc_text = doc_text.split()
	
	doc_name = ntpath.basename(doc_name)
	#stemming words
	doc_text = [stem(w) for w in doc_text]


	#stop word removal
	doc_text= [w for w in doc_text if w not in Stop_Word.objects.filter(word=w)]

	
	#add words to database
	for loc,word in enumerate(doc_text):
		obj = Inv_Index()
		obj.word = word
		obj.doc_name = doc_name
		obj.word_pos = loc
		obj.save()

		try:
			obj1 = term_Frequency.objects.get(word=word,doc_name=doc_name)
			obj1.word_freq +=1	
			obj1.save()
		except:
			obj1 = term_Frequency()
			obj1.word = word
			obj1.doc_name = doc_name
			obj1.word_freq = 1
			obj1.save()


			
	#normalize term frequency
	normalize = 0
	
	for obj in term_Frequency.objects.filter(doc_name = doc_name):
		normalize += (obj.word_freq**2)
	
	normalize = sqrt(normalize)
	
	#calculating term frequency
	for obj in term_Frequency.objects.filter(doc_name = doc_name):
		obj.term_freq = obj.word_freq/normalize
		obj.save()

	print "Done indexing: "+doc_name


@login_required
def index_all(request):

	if request.method == "GET":
		#site_root = os.path.dirname(os.path.realpath(__file__))
		html_files = os.getcwd()+'/searchengine/static/html_files'	
		file_list = glob.glob( os.path.join(html_files, '*.html') )
		N = len(file_list)+0.0

		for file_iterator in file_list:
			Index(file_iterator)

		#calculating Inverted Document frequency
		

		for obj in term_Frequency.objects.all():
		
			try:
				idf_obj = IDF.objects.get(word=obj.word)
			except:
				idf_obj = IDF()
				idf_obj.word = obj.word

				idf_obj.idf = N/len(term_Frequency.objects.filter(word = obj.word))
				idf_obj.save()

			obj.tf_idf = obj.term_freq * idf_obj.idf
			obj.save()
		
		
		
		#print l			
		return HttpResponse("Indexing Done!!!")





@login_required
def index(request):
	if request.method == "POST":
		return HttpResponse(request)
	else:
		return render_to_response("indexer.html", {
			'user_logged':request.user.username
	        }, context_instance=RequestContext(request))


@login_required
def stop_word(requests):
	stop_word_call()	
	return HttpResponse("Stop Words Updated")	



#to load stop_words to database!!!!
def stop_word_call():
	with open(os.getcwd()+'/searchengine/misc_files/stop_words.txt') as f:
		for s in f.readlines():
			try:
				obj = Stop_Word.objects.get(word=s.strip())		
			except:
				obj = Stop_Word(word = s.strip())
				obj.save()
			


	


'''
@login_required
def index_file(request, slug):
	site_root=os.path.dirname(os.path.realpath(__file__))
	html_files = os.path.join(site_root, '../static/html_files')

	file_list = glob.glob( os.path.join(html_files, '*.html') )

	slug_file = html_files+"\\"+slug

	if slug_file in file_list:
		with open(slug_file, 'rb') as f:
			for line in f.readlines():
				Index(line, slug_file.replace(html_files + "\\", ''))
		return HttpResponse('indexed')
	else:
		return HttpResponse('not there')


'''
