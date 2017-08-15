import math
import pickle
import os
from collections import Counter
from config import DIC_FILE, AFF_FILE
from hunspell import HunSpell 

symbols = [',', '.', ';', '\'', '"', '{', '}', '[', ']', '(', ')', '?', ':', '*', '^', '-', '%', '\\', '/']

hunspell_object = HunSpell(DIC_FILE, AFF_FILE)

class GFG:

	def __init__(self):
		print "Done"
        
       
	def stem(self, hunspell_object, word):
    		stemmed_list = hunspell_object.stem(word)
    		if len(stemmed_list) > 0:
        		return str(stemmed_list[0])

 

	def index(self, words_file):
		open_file = open(words_file, 'r')
		words_list =[]
		contents = open_file.readlines()

		for i in range(len(contents)):
                    for s in symbols:
                        contents[i] = contents[i].replace(s, ' ')
                    words_list.extend(contents[i].split())
		return words_list    

	def create(self, documents): 
                doc_len = {}        
                dict = {}
		for doc in documents:
			wordlist = self.index(doc)
                        doc_len[doc] = len(wordlist)
			for word in wordlist:
                                word = word.lower()
#				word = str(self.stem(hunspell_object, word.encode('string-escape')))
                                if word in dict:
			            dict[word].append(doc)
				else:
			            dict[word] = []
        			    dict[word].append(doc)
                num_of_doc = {}
                for k in dict:
                    dict[k].sort()
                    dict[k] = Counter(dict[k]).items() 
                    num_of_doc[k] = len(dict[k])
                    dict[k] = sorted(dict[k], key = lambda x: x[1])[-9:]
                    dict[k].reverse()
                return (dict, num_of_doc, doc_len)


documents=os.listdir("texts")
obj = GFG()
os.chdir("texts")
(dictionary, num_of_doc, doc_len) = obj.create(documents)
#print dictionary

#print idf
#f = open('a.txt', 'w')
#for i in sorted(dictionary):
#    f.write(i + " ")
#    for j in dictionary[i]:
#    	f.write(j + " ")
#    f.write("\n")
os.chdir("..")
with open("inverted_index.pickle", 'wb') as h:
        pickle.dump(dictionary, h, protocol=pickle.HIGHEST_PROTOCOL)
with open("num_of_doc.pickle", 'wb') as h:
        pickle.dump(num_of_doc, h, protocol=pickle.HIGHEST_PROTOCOL)
with open("doc_len.pickle", 'wb') as h:
        pickle.dump(doc_len, h, protocol=pickle.HIGHEST_PROTOCOL)

