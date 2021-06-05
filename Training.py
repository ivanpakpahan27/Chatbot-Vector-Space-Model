import numpy as np
np.seterr(divide='ignore', invalid='ignore')
import string
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from tkinter import *
from collections import *
import glob
import os

def describe(file_path):
    vec =[]
    docs=[]
    anti_dup=[]

    with open(file_path) as rf, open("out.txt", "w") as wf:
        for line in rf:
            wf.write("%s " % line.strip())
    ekstrak = open("out.txt", "r")
    doc = ekstrak.read()
    doc = doc.replace('/', ' . ')
    doc = doc.replace('-', ' . ')
    doc = doc.translate(str.maketrans('', '', string.punctuation)).lower()
    doc = re.sub('[0-9]+', '', doc)
    doc = doc.split(' ')
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    for j in range(len(doc)):
        dasar = stemmer.stem(doc[j])
        docs.append(dasar)
        continue
    '''for i in range(len(anti_dup)):
        vector = Counter(docs).most_common()
        d = {}
        for w in vector:
            d[w[0]] = w[1]
        try:
            vector_q = d[anti_dup[i]]
        except KeyError as d:
            vector_q = 0
        vec.append(vector_q)'''
    removal = []
    clear   = []
    stoplist = os.path.join("stopword.txt")
    stoplist = np.genfromtxt(stoplist, dtype='str')
    for i in range(len(docs)):
        if docs[i] in stoplist:
            removal.append(docs[i])
        else:
            clear.append(docs[i])
    return clear

output = open("Index.csv", "w")
for docPath in glob.glob("Documents/*"):
    docID = docPath[docPath.rfind("/") + 1:]
    file_path = str(docPath)
    doc = describe(file_path)
    output.write("%s,%s\n" % (docID, ",".join(doc)))
output.close()

