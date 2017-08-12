class search:
	def __init__(self):
		print "searching"

	def find(self, word):
		fp=open("a.txt", "r")
		fp.seek(0,2)
		begin = 0
		end = fp.tell()
		while (begin<end):
		    fp.seek((end - begin) / 2, 0)
    		fp.readline()
    		line = fp.readline()
    		line_key = line.partition(' ')[0]
    		print line_key
    		if (word == line_key):
        		for x in line.partition(' ')[1:]:
        			print x
    		elif (word > line_key):
        		begin = fp.tell()
    		else:
        		end = fp.tell()


d = search()
d.find("rajan")
