import os
import pickle
links = open("links.txt")
os.chdir("../corpus")
with open("links_map.pickle", "rb") as h:
    m = pickle.load(h)

i = 10000
for link in links:
    i = i+1
    ll = link.rstrip("\n\r ")
    pr = "wget -O " + str(i) + " " + ll
    print "\n\n" + str(len(m)) + "\n\n"
    m[str(i)] = ll
    os.popen(pr)



with open("links_map.pickle", "wb") as handle:
    pickle.dump(m, handle, protocol = pickle.HIGHEST_PROTOCOL)
