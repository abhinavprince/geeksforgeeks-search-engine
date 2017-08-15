file = open('1.txt','r')
word = "rajan"

doc = []
for line in file:
	for ex in line.split():
		doc.append(ex)

i= 0
for i in range(len(doc)):
	if doc[i] == word:
		s = doc[i:i+4]
		print ' '.join(s), 