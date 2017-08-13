import math
import pickle
import os
from collections import Counter

symbols = [',', '.', ';', '\'', '"', '{', '}', '[', ']', '(', ')', '?', ':', '*', '^', '-', '%']

class GFG:

	def __init__(self):
		print "Done"

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
                dict = {}
		for doc in documents:
			wordlist = self.index(doc)
			for word in wordlist:
                                word = word.lower()
				if word in dict:
					dict[word].append(doc)
				else:
					dict[word] = []
					dict[word].append(doc)
                
                idf = {}
                for k in dict:
                    dict[k].sort()
                    dict[k] = Counter(dict[k]).items() 
                    idf[k] = math.log(17444/len(dict[k]))
                    dict[k] = sorted(dict[k], key = lambda x: x[1])[-9:]
                    dict[k].reverse()
                return (dict, idf)


documents=os.listdir("texts")
obj = GFG()
os.chdir("texts")
(dictionary, idf) = obj.create(documents)
print dictionary

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
with open("idf.pickle", 'wb') as h:
        pickle.dump(idf, h, protocol=pickle.HIGHEST_PROTOCOL)


