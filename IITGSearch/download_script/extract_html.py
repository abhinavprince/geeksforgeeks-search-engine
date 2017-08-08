import os
links = open("links.txt", "a")

bad_ex = ["bmp", "jpg", "jpeg", "GIF", "gif", "pdf", "zip", "png"]

with open("unique_links.txt") as f:
        for line in f:
            fl = True
            for ex in bad_ex:
                if ex in line:
                    fl = False

            if fl:
                links.write(line)
                
