import math, sys, os


scriptDir = os.path.dirname(__file__)
# lemmaHandle = open(os.path.join(scriptDir, 'lemmata.csv'), 'r')
# stopwordHandle = open(os.path.join(scriptDir, 'stopwords.txt'), 'r')

def importStopwords(handle):
	# import stopwords from file
	stopwords = []
	for line in handle:
		if len(line.split()) == 0 or line[0] == '#':
			continue
		stopwords.append(line.split()[0])
	return stopwords


def lemmatize(text, lemmata):
	# lemmatize text
	for i in range(0,len(text)):
		if text[i] in lemmata:
			text[i] = lemmata[text[i]]
	
	# don't return any single letters
	text = [t for t in text if len(t) > 1]
	return text

def removeStopwords(text, stopwords):
	# remove stopwords
	content = [w for w in text if w not in stopwords]
	return content

def tokenize(text):
	# remove punctuation, tokenize
	return "".join(c if c.isalpha() else ' ' for c in text).split()

def isNoun(word): # pseudo check if given word is a noun (if it has a capital letter, so sometimes this method returns some garbage)
	return (len(word)>=1 and word[0].isupper())



def analyze(documents, resultsPerDocument=-1, preferNouns=False, ranking=True, files=False, verbose=False):
	
	if verbose:
		print('Initializing..')

	# load language data
	# stopwords = importStopwords(stopwordHandle)

	localWordFreqs = {}
	globalWordFreq = {}

	if verbose:
		print('Working through documents.. ')

	progress = 0;

	for doc in documents:
		# calculate progress
		progress += 1
		if progress%math.ceil(float(len(documents))/float(20)) == 0:
			if verbose:
				print(str(100*progress/len(documents))+'%')
		
		# local term frequency map
		localWordFreq = {}
		localWords = doc
		if files:
			localWords = open(doc, 'r').read()
		localWords = tokenize(localWords)
		# localWords = removeStopwords(localWords, stopwords)
		
		# increment local count
		for word in localWords:
			if word in localWordFreq:
				localWordFreq[word] += 1
			else:
				localWordFreq[word] = 1

		# increment global frequency (number of documents that contain this word)
		for (word,freq) in localWordFreq.items():
			if word in globalWordFreq:
				globalWordFreq[word] += 1
			else:
				globalWordFreq[word] = 1

		localWordFreqs[doc] = localWordFreq


	if verbose:
		print('Calculating.. ')

	results = []
	for doc in documents:
		if files:
			writer = open(doc + '_tfidf', 'w+')
		result = []
		# iterate over terms in f, calculate their tf-idf, put in new list
		for (term,freq) in localWordFreqs[doc].items():
			nounModifier = 1 + int(preferNouns)*int(isNoun(term))*0.3
			tf = float(1 + math.log(float(freq)))
			idf = math.log(float(len(documents)) / float(globalWordFreq[term]))
			tfidf = float(tf) * float(idf) * nounModifier
			result.append([tfidf, term])

		# sort result on tfidf and write them in descending order
		result = sorted(result, reverse=True)
		if files:
			for (tfidf, term) in result[:resultsPerDocument]:
				if ranking:
					writer.write(term + '\t' + str(tfidf) + '\n')
				else:
					writer.write(term + '\n')
		else:
			if not ranking:
				res = []
				for re in result:
					res.append(re[1])
				results.append(res[:resultsPerDocument])
			else:
				results.append(result[:resultsPerDocument])

	if verbose:
		print('Success, with ' + str(len(documents)) + ' documents.')

	return results


documents = []
documents.append("1.txt")
documents.append("2.txt")
analyze(documents, -1, False, True, True, False)

