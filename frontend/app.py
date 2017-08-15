# import the Flask class from the flask module
from flask import Flask, session, render_template, redirect, url_for, request,  Response
from flaskext.mysql import MySQL
from flask_session import Session
import MySQLdb
from flask_pymongo import PyMongo
import json
from py2neo import Graph, authenticate
from py2neo import Node, Relationship

import re
from collections import Counter


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

    l = stem_query(q)
    
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
		word = query.split()
		doc = []
		for line in file:
			for ex in line.decode('utf-8').split():
				doc.append(ex)
		#print doc
		for k in range(500 ,len(doc)):
			if doc[k].lower() in word:
				#print doc[k]
				s = doc[k:k+4]
				if len(stri) > 200:
					break
				stri += ' '.join(s)
		c.append(stri)
		file.close()
	d = []
	for j in y:
		stri = ""
		file = open(os.path.join('texts/', j[0]),'r')
		word = query.split()
		doc = []
		for line in file:
			for ex in line.decode('utf-8').split():
				doc.append(ex)

		for k in range(500, len(doc)):
			if doc[k].lower() in word:
				s = doc[k:k+4]
				if len(stri) > 200:
					break
				stri += ' '.join(s)
		d.append(stri)
		file.close()
	m = []
	n = []
	for i in range(len(a)):
		m.append({'ab':a[i], 'cd':c[i]})
	for i in range(len(b)):
		n.append({'ab':b[i], 'cd':d[i]})
	print m
	return render_template('index.html', name1= m, name2=n)

@app.route('/search',methods = ['POST', 'GET'])
def search():
	user="hello"
	if request.method=="POST":
		user = request.form['nm']
	return redirect(url_for('success',query = user))


@app.route('/home')
def home():
	return render_template('index.html')


if __name__ == '__main__':
#	app.secret_key = 'qwerty'
	app.run(host='0.0.0.0', debug=True)
