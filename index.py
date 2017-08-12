import bm25
import tf_idf

class GFG:

	def __init__(self):
		print "Done"

	def index(self, words_file):
		open_file = open(words_file, 'r')
		words_list =[]
		contents = open_file.readlines()
		for i in range(len(contents)):
			words_list.extend(contents[i].split())
		return words_list    
		open_file.close()

	def create(self, documents ,dict):
		for doc in documents:
			wordlist = self.index(doc)
			for word in wordlist:
				if word in dict:
					dict[word].append(doc)
				else:
					dict[word] = []
					dict[word].append(doc)
		return dict


dictionary = {}
documents=[]
documents.append('1.txt')
documents.append('2.txt')
obj = GFG()
dictionary = obj.create(documents, dictionary)
f = open('a.txt', 'w')
for i in sorted(dictionary):
    f.write(i + " ")
    for j in dictionary[i]:
    	f.write(j + " ")
    f.write("\n")