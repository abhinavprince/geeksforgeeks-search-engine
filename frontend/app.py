# import the Flask class from the flask module
from flask import Flask, session, render_template, redirect, url_for, request,  Response, Markup
from flask_session import Session
import json

import re
from collections import Counter

from autocorrect import spell
import sys, os
import pickle
import operator
import math

from config import DIC_FILE, AFF_FILE

try:
    from hunspell import HunSpell
except ImportError:
    sys.stderr.write("error: %s\n" % "Can't import hunspell module!!!")
    sys.exit(1)

from googleapiclient.discovery import build
import pprint

my_api_key = "AIzaSyDhxdW5w8MKtzXhqdP_ifSJIiJgZaDLUUg"
my_cse_id = "008408648827036128353:hfsq9opynu4"

def google_search(search_term, api_key, cse_id, **kwargs):
	service = build("customsearch", "v1", developerKey=api_key)
	res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
	return res['items']


def tokenize(text):
    # remove punctuation, tokenize
    return "".join(c if c.isalpha() else ' ' for c in text).split()


def stem(hunspell_object, word):
    stemmed_list = hunspell_object.stem(word)
    if len(stemmed_list) > 0:
        return str(stemmed_list[0])
    else:
        return word

dummy_words = ['of', 'the', 'in', 'is', 'was', 'to', 'from']

def stem_query(query):
    # returns list of stemmed words

    hunspell_object = HunSpell(DIC_FILE, AFF_FILE)

    stemmed_list = []

    tokens = tokenize(query)
    for word in tokens:
        if word not in dummy_words:
            stemmed_list.append(stem(hunspell_object, word))
    
    return stemmed_list

with open("inverted_index.pickle") as h:
    inv = pickle.load(h)

with open("num_of_doc.pickle") as h:
    num_of_doc = pickle.load(h)

with open("doc_len.pickle") as h:
    doc_len = pickle.load(h)

with open("links_map.pickle") as h:
    l_m = pickle.load(h)

idf = {}
for k in inv:
    idf[k] = math.log(17444/num_of_doc[k])

k1 =  1.5
b1 = .75

ss = 0
for k, v in doc_len.iteritems():
    ss += v

avgl = ss/5000

def ranking(q):

	m = stem_query(q)
	l = []
	for word in m:
		if word not in dummy_words:
			l.append(word)
    
	print l
	scores = {}
	for term in l:
		if term in inv:
			for (doc, tf) in inv[term]:
				if doc in scores:
					scores[doc] = scores[doc]+tf*idf[term]
				else:
					scores[doc] = tf*idf[term]
	tf_score = sorted(scores.items(), key=operator.itemgetter(1))
	tf_score.reverse()
	scores = {}

	for term in l:
		if term in inv:
			for (doc, tf) in inv[term]:
				sc = (tf*(k1+1))/(tf + k1*(1-b1+b1*(doc_len[doc]/avgl)))
				if doc in scores:
					scores[doc] = scores[doc]+idf[term]*sc
				else:
					scores[doc] = idf[term]*sc
   
	okapi_score = sorted(scores.items(), key=operator.itemgetter(1))
	okapi_score.reverse()

	return (tf_score, okapi_score)



app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"

@app.route('/success/<query>')
def success(query):
	dym = ""
	temp = query.split()
	for  i in range(len(temp)):
		temp[i] = spell(temp[i])
	if query != ' '.join(temp):
		dym = ' '.join(temp)

	print "|||   " + dym + "  ||||||||||"

	x , y = ranking(query)
	a=[]
	b=[]
	for i in x:
		a.append(l_m[i[0]])
	for j in y:
		b.append(l_m[j[0]])
	c = []
	for i in x:
		stri = ""
		file = open(os.path.join('texts/', i[0]),'r')
		l = query.split()
		word = []
		for ass in l:
			if ass not in dummy_words:
				word.append(ass)
		doc = []
		for line in file:
			for ex in line.decode('utf-8').split():
				doc.append(ex)
		#print doc
		for k in range(500 ,len(doc)):
			if doc[k].lower() in word:
				#print doc[k]
				doc[k] = "<b>" + doc[k]+ "</b>"
				s = doc[k:k+4]
				if len(stri) > 350:
					break
				stri += ' '.join(s) + "..."
		c.append(Markup(stri))
		file.close()
	d = []
	for j in y:
		stri = ""
		file = open(os.path.join('texts/', j[0]),'r')
		l = query.split()
		word = []
		for ass in l:
			if ass not in dummy_words:
				word.append(ass)
		doc = []
		for line in file:
			for ex in line.decode('utf-8').split():
				doc.append(ex)

		for k in range(500, len(doc)):
			if doc[k].lower() in word:
				doc[k] = "<b>" + doc[k]+ "</b>"
				s = doc[k:k+4]
				if len(stri) > 350:
					break
				stri += ' '.join(s) + "..."
		d.append(Markup(stri))
		file.close()
	m = []
	n = []
	m_ls = []
	n_ls = []
	for i in range(len(a)):
		m.append({'ab':a[i], 'cd':c[i]})
		m_ls.append(a[i])
	for i in range(len(b)):
		n.append({'ab':b[i], 'cd':d[i]})
		n_ls.append(b[i])
	results = google_search(query, my_api_key, my_cse_id, num=10)
	listy=[]
	for result in results:
		listy.append(result['formattedUrl'])

	m_ls = m_ls[0:5]
	n_ls = n_ls[0:5]
	print m_ls
	print n_ls
	count_tf=0
	count_bm=0
	for obj in listy:
		obj = "http://" + obj
		if obj in m_ls:
			count_tf += 1
		if obj in n_ls:
			count_bm += 1

	return render_template('index.html', name1= m, name2=n, name3=listy, count1=count_tf+1, count2= count_bm+1, word_list=word, did=dym)

@app.route('/search',methods = ['POST', 'GET'])
def search():

	if request.method=="POST":
		user = request.form['nm']
	return redirect(url_for('success',query = user))


@app.route('/home')
def home():
	return render_template('index.html')


if __name__ == '__main__':
	app.run(host='0.0.0.0',port=6969, debug=True)
