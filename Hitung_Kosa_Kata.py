import glob
import os
import string
from tkinter import *
a =[]
for docPath in glob.glob("Documents/*"):
    docID = docPath[docPath.rfind("/") + 1:]
    file_path = str(docPath)
    with open(file_path) as rf, open("test.txt", "w") as wf:
        for line in rf:
            wf.write("%s " % line.strip())
            line = line.replace('-',' ')
            line = line.replace('?',' ')
            line = line.replace('/',' ')
            line = line.replace(':', ' ')
            line = line.replace('.', ' ')
            line = re.sub('[0-9]+', '', line)
            line = line.split()
            for i in line :
                if i not in a:
                    a.append(i)
print(a)
print(len(a))