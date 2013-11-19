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


from collections import defaultdict
import os,sys
import re
import glob
import pickle
from stemming.porter2 import stem
from bs4 import BeautifulSoup
from django.utils.encoding import smart_str


from searchengine.indexer.models import *
from searchengine.search.models import *


def ranking(query,doc_list):
	query.sort()
	doc_vector = []
	
	
	for doc in doc_list:
		obj = term_Frequency.objects.filter(doc_name = doc).order_by('word')
		doc_vector.append([(i.word,i.word_freq) for i in obj])
		
		
	
	query_vector = defaultdict(int)
	
	for i in query: query_vector[i]+=1
	
	query_vector = [(i,query_vector[i]) for i in query_vector.keys()]
	
	
	
def process_results(results,q):
	html_files = os.getcwd()+'/searchengine/static/html_files'

	result_list = []
	for i in results:
		r = {}
		r['link']= i

		soup = BeautifulSoup(open(html_files+'/'+i))
		r['title'] = smart_str(soup.title.text)

		content = smart_str(soup.body.text) # parse body only
		content = (content + ' ' + smart_str(soup.title.text)).lower()
		content = re.sub(r'[^0-9a-z]',' ',content)
		content = content.split()
		
			#stemming words
		content = [stem(w) for w in content]

		
	
		index = content.index(smart_str(q[0]))
		start = index-10
		end = index + 10		
		
		if start < 0 : start = 0
		if end >= len(content): end = len(content)-1		
		
		r['content'] = ' '.join(content[start:end+1])
		result_list.append(r)

	return result_list

def home(request):
	
	q_words=''
	word = ''
	if request.method == "POST":
		def Process_Word(words):
			
			words = words.lower()
			words = re.sub(r'[^0-9a-z]',' ',words)
			words = words.split()
			
			#stemming words
			words = [stem(w) for w in words]

			#stop word removal
			words = [w for w in words if w not in Stop_Word.objects.filter(word=w)]

			
			return words



		search_results = defaultdict(int)

		
		query= []
		word = request.POST['q']
		q_words = word
		m = re.search(r'"$',word)
		if m is None:
			case = 2
		else:
			case = 3
			word = word.strip('"')
		query = Process_Word(word)

		if len(query)==	1: case =1

		# for single word or multiple word		

		if case ==1 or case==2:
		
			try:
				for word in query:
					for obj in Inv_Index.objects.filter(word=word):
						search_results[obj.doc_name]=1
					
			except:
				search_result={}
			results = list(search_results)

		if case ==3:
			
			doc_list=[]
			for word in query:
				w = Inv_Index.objects.filter(word=word).values_list('doc_name').distinct()
				for i in w:	search_results[i[0]]+=1
			

			for i in search_results:
				if search_results[i]==len(query):
					doc_list.append(i)
			
			
			results=[]
			for doc in doc_list:
				n=[]
				in_order = set()
				for word in query:
					n.append([i.word_pos for i in Inv_Index.objects.filter(word=word,doc_name=doc)])		
			
				n = [[x-i for x in n[i] ]for i in range(len(n))]
				in_order = set(n[0]).intersection(*n[1:])
				
				if in_order:results.append(os.getcwd()+'/searchengine/static/html_files/' + doc) 			
			

		


		if len(results)==0:
			results = 'Not Found'
		else:
			results = process_results(results,query)
				
		
		
	else:
		results = None
	return render_to_response("search.html", {'results': results,'query':q_words,'user_logged': request.user.username}, context_instance=RequestContext(request))
	

def view_file(request, slug):
	html_files = os.getcwd()+'/searchengine/static/html_files'
	slug_file = html_files+"/"+slug

	with open(slug_file, 'rb') as f:
		content = "\n".join(f.readlines())
	return HttpResponse(content)

	
