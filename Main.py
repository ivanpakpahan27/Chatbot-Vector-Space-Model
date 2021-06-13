import os
import numpy as np
np.seterr(divide='ignore', invalid='ignore')
import nltk
import string
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from tkinter import *
from collections import *
import collections
import math
import random
import winsound
import time
import csv
from datetime import datetime

def respon_waktu():
    waktu_lokal = time.localtime(time.time())
    respon= ['Selamat Tengah Malam', 'Selamat Pagi', 'Selamat siang','Selamat Sore','Selamat Malam']
    jam = waktu_lokal.tm_hour
    if 0 <= jam < 6:
        Chat_bot = respon[0]
    elif 6 <= jam < 10:
        Chat_bot = respon[1]
    elif 10 <= jam < 13:
        Chat_bot = respon[2]
    elif 13 <= jam < 17:
        Chat_bot = respon[3]
    elif 17 <= jam < 24:
        Chat_bot = respon[4]
    return (Chat_bot)

def respon_salam():
    respon  = ["Halo", "Hi", "Hola", "Hey", "Helo", "Hello"]
    Chat_bot =  random.choice(respon)
    return (Chat_bot)

def respon_baik():
    respon = ["Sama-sama", "You're welcome", "oke, sama-sama", "Siap", "Thank you too", "Baiklah"]
    Chat_bot =  random.choice(respon)
    return (Chat_bot)

def respon_buruk():
    respon = ["Maaf, kemampuan saya terbatas","Mungkin, chat kamu kurang spesifik","Chat kamu mungkin diluar jangkauan saya","Sorry","Sorry, I can't handle it"]
    Chat_bot =  random.choice(respon)
    return (Chat_bot)

def respon_pengetahuan(chat) :
    respon    = ["Chat kamu kurang detail", "Saya tidak memahami chat kamu", "Tolong perjelas chatnya yah..","Saya kurang paham terhadap chat kamu"]
    respon_2  = ["Maaf, saya tidak paham", "Saya tidak bisa menjawabnya","Kecerdasan saya terbatas, saya tidak memahaminya", "Maaf, tolong perjelas chat kamu"]
    result    = []
    vek_kueri = []
    sumA      = []
    a         = []
    docs      = []
    vec       = []
    setData   = []
    removal   = []
    clear     = []
    anti_dup  = []
    sumC      = []
    c         = []
    kiri      = []
    e         = []
    full      = []
    #A. Preprocessing
    #1. Case Folding
    chat = chat.translate(str.maketrans('','',string.punctuation)).lower()
    chat = re.sub('[0-9]+', '',chat)
    case = re.sub('\n+','',chat)
    #2. Tokenization
    tokens = nltk.tokenize.word_tokenize(case)
    #3. Filtering
    stoplist = os.path.join("stopword.txt")
    stoplist = np.genfromtxt(stoplist, dtype='str')
    for i in range(len(tokens)):
        if tokens[i] in stoplist:
            removal.append(tokens[i])
        else:
            clear.append(tokens[i])
    #4. Stemming
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    for i in range(len(clear)):
        kata = stemmer.stem(clear[i])
        result.append(kata)
    for i in result:
        if i not in anti_dup:
            anti_dup.append(i)
    vektor_kueri=collections.Counter(result).most_common()
    for kata in vektor_kueri:
        vek_kueri.append(kata[1])
    if len(anti_dup)<2:
        Chat_bot =  random.choice(respon)
    else:
        # B. Open dokumen & VSM
        # 1. Pilih dokumen & Preprocessing
        path, dirs, files = next(os.walk("Documents"))
        jlh = len(files)
        for i in range(jlh):
            chat_path = ('Chat/Dokumen' + str(i) + '.txt')
            setData.append(chat_path)
            with open("Index.csv") as f:
                reader = csv.reader(f)
                for row in reader:
                    docs = [str(x) for x in row[1:]]
                    docky = [str(x) for x in row[0]]
                    docse = ','.join(docky)
                    docse = docse.replace(',', '')
                    docse = docse.replace('Documents\\', 'Chat\\')
                    full.append(docse)
                    for i in range(len(anti_dup)):
                        vector = Counter(docs).most_common()
                        d = {}
                        for w in vector:
                            d[w[0]] = w[1]
                        try:
                            vector_q = d[anti_dup[i]]
                        except KeyError as d:
                            vector_q = 0
                        vec.append(vector_q)
                    docs.clear()
        vek_d = np.array(vec)
        vek_dokumen = np.reshape(vek_d, (-1,len(anti_dup)))
        '''print(vec)
        print(anti_dup)
        print(vek_dokumen)
        print(vector)'''
        #Process
        for i in range(len(vek_dokumen)):
            for j in range(len(vek_dokumen[i])):
                x = vek_dokumen[i][j] * vek_kueri[j]
                a.append(x)
            b = np.sum(a)
            sumA.append(b)
            a.clear()
            b = 0
        for i in range(len(vek_dokumen)):
            for j in range(len(vek_dokumen[i])):
                x = vek_dokumen[i][j]*vek_dokumen[i][j]
                c.append(x)
            b = np.sum(c)
            sumC.append(b)
            c.clear()
            b = 0
        for i in sumC:
            s = math.sqrt(i)
            kiri.append(s)
        for i in range(len(vek_kueri)):
            x = vek_kueri[i]*vek_kueri[i]
            e.append(x)
        akar_kueri = np.sum(e)
        akar_kueri = math.sqrt(akar_kueri)
        sumA = np.array(sumA)
        kiri = np.array(kiri)
        bawah = kiri * akar_kueri
        final = sumA/bawah
        antiZero = final.tolist()
        antiZero = [0 if math.isnan(x) else x for x in antiZero]
        hasil = antiZero.index((max(antiZero)))
        if antiZero[hasil]>0:
            hasil = open(full[hasil],"r")
            Chat_bot = hasil.read()
        else:
            Chat_bot = random.choice(respon_2)
        print(antiZero)
        print(hasil)
    return (Chat_bot)

root = Tk()
root.config(bg="lightblue")
root.title("Chatbot Mr S Ahli Sejarah VOC")
bg = PhotoImage(file = "images/bot.png")
canvas = Canvas(root, width=550, height=550,bg="silver")
canvas.create_image( 0, 0, image = bg,anchor = "nw")
canvas.grid(row=0,column=0,columnspan=2)
bubbles = []
class BotBubble:
    def __init__(self,master,message=""):
        self.master = master
        self.frame = Frame(master,bg="light blue")
        self.i = self.master.create_window(300,360,window=self.frame)
        Label(self.frame,text=datetime.now().strftime("%Y-%m-%d %H:%M"),font=("Times", 7),bg="light blue").grid(row=0,column=0,sticky="w",padx=5)
        Label(self.frame, text=message,font=("Times", 9),bg="light blue").grid(row=1, column=0,sticky="w",padx=5,pady=3)
        root.update_idletasks()
        self.master.create_polygon(self.draw_triangle(self.i), fill="light blue", outline="light blue")
    def draw_triangle(self,widget):
        x1, y1, x2, y2 = self.master.bbox(widget)
        return x1,y2,x1,y2,x1,y2
class BotBubble_Send:
    def __init__(self,master,message=""):
        self.master = master
        self.frame = Frame(master,bg="light green")
        self.i = self.master.create_window(90,360,window=self.frame)
        Label(self.frame,text=datetime.now().strftime("%Y-%m-%d %H:%M"),font=("Times", 7),bg="light green").grid(row=0,column=0,sticky="w",padx=5)
        Label(self.frame, text=message,font=("Times", 9),bg="light green").grid(row=1, column=0,sticky="w",padx=5,pady=3)
        root.update_idletasks()
        self.master.create_polygon(self.draw_triangle(self.i), fill="light green", outline="light green")
    def draw_triangle(self,widget):
        x1, y1, x2, y2 = self.master.bbox(widget)
        return x1, y2 - 5, x1 - 50, y2 + 10, x1, y2
def receive_message(respon):
    if bubbles:
        canvas.move(ALL, 0, -65)
        canvas.create_image(0, 0, image=bg, anchor="nw")
    a = BotBubble(canvas,message=respon)
    bubbles.append(a)
def masuk(chat):
    print("Mr Sejarah : Halo.., saya akan membantu kamu, menjawab seputar sejarah VOC di Indonesia")
    print("Mr Sejarah : Kalau jawaban yang kamu cari tidak tepat, tolong perjelas lagi pertanyaan kamu")
    chat = chat.translate(str.maketrans('','',string.punctuation)).lower()
    waktu = ["pagi","siang","malam","sore"]
    salam = ["halo", "hii", "hola", "hey", "helo", "hello","namaku"]
    baik  = ["terimakasih", "bermanfaat", "berguna", "makasih", "thanks", "thx"]
    buruk = ["kok tidak","wah kurang","tidak jelas","kurang paham","tidak paham","tidak akurat"]
    if any(word in chat for word in waktu):
        print(respon_waktu())
        pesan = respon_waktu()
        receive_message(pesan)
        winsound.PlaySound("Music/rec.wav", winsound.SND_FILENAME)
    elif any(word in chat for word in salam):
        print(respon_salam())
        pesan = respon_salam()
        receive_message(pesan)
        winsound.PlaySound("Music/rec.wav", winsound.SND_FILENAME)
    elif any(word in chat for word in buruk):
        print(respon_buruk())
        pesan =  respon_buruk()
        receive_message(pesan)
        winsound.PlaySound("Music/rec.wav", winsound.SND_FILENAME)
    elif any(word in chat for word in baik):
        print(respon_baik())
        pesan = respon_baik()
        receive_message(pesan)
        winsound.PlaySound("Music/rec.wav", winsound.SND_FILENAME)
    else:
        print(respon_pengetahuan(chat))
        pesan = respon_pengetahuan(chat)
        receive_message(pesan)
        winsound.PlaySound("Music/rec.wav", winsound.SND_FILENAME)
    return(pesan)
def send_message():
    if bubbles:
        canvas.move(ALL, 0, -65)
        canvas.create_image(0, 0, image=bg, anchor="nw")
    a = BotBubble_Send(canvas,message=entry.get())
    chat = entry.get()
    masuk(chat)
    bubbles.append(a)
entry = Entry(root,width=60,font="Times")
entry.grid(row=1,column=0)
Button(root,text="Send",command=send_message,width = 5,font="Times").grid(row=1,column=1)
root.mainloop()
