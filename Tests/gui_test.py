from tkinter import *
from tkinter import filedialog
from math import *
import hashlib
import os

def decodeFromFile(path):
    result = []
    file = open(path, encoding="latin_1")
    data = file.readlines()
    data = [x.strip().split() for x in data]
    for i in range(1, len(data)):
        data[i][1] = float(data[i][1])
    lenght = int(data[0][0])
    data = sorted(data[1:], key=lambda x: x[1], reverse=True)
    file.close()
    return data

def replaceSpecChr(string):
    spec = ['é', 'è', 'ê', 'à', 'ù', 'û', 'ç', 'ô', 'î', 'ï', 'â']
    safe = ['e', 'e', 'e', 'a', 'u', 'u', 'c', 'o', 'i', 'i', 'a']
    i = 0
    while i < len(spec):
        string = string.replace(spec[i], safe[i])
        i += 1
    return string

def makeStats(path):
    # Creation du fichier statistique
    #ouverture
    file = open(path, encoding="latin_1")
    chain = replaceSpecChr(file.read().lower())

    chainLen = len(chain)
    file.close()

    #generation
    dico = {}
    for letter in chain:
        if (letter in dico):
            dico[letter] += 1
        elif (letter != " " and letter != "\n"):
            dico[letter] = 1

    #sauvegarde
    saveTo = hashlib.md5()
    saveTo.update(path.encode('utf-8'))
    saveTo = "statistics/" + saveTo.hexdigest() + ".dat"
    output = str(chainLen) + "\n"
    for key in dico:
        output += key + " " + str(dico[key]/chainLen) + "\n"
    save = open(saveTo, mode="w")
    save.write(output)
    save.close()
    return saveTo

def displayStats(path):
    global data, rows, info, infoLabel
    data = decodeFromFile(path)
    rows = []

    #Create interface
    chart.create_line(20, 0, 20, 400, fill="#555555")
    for i in range(1, ceil(560/80)):
        x = 21 + i * 80
        chart.create_line(x, 10, x, 390, fill="#888888")
        chart.create_text(x, 395, text=str(int((((x-21)/560)*maxValue)*10000)/100) + " %", fill="#333333")
        
    #Create rows
    for i in range(len(data)):
        rows.append(Row(i-1, data[i]))
        
    for e in range(50):
        for i in range(len(data)):
            rows[i].animate()
            chart.update()

    #Create info
    info = chart.create_rectangle(10000, 5000, 16000, 3000, fill="#DDDDDD" , outline="#555555")
    infoLabel = chart.create_text(10000, 5000, text="null")

    #Create handler
    chart.bind("<Motion>", motionHandler)

def load():
    path = filedialog.askopenfilename(initialdir=os.getcwd() + "/librairie/", title="Analyse frequencielle", filetypes=[("Text Files", "*.txt")])
    if (path != ""):
        titleLabel.config(text=path)
        generated = makeStats(path)
        displayStats(generated)
    else:
        print("aborted")

def motionHandler(e):
    global data
    y = e.y
    identifier = y // 15
    infoX = e.x - 30
    if (identifier == 0 or identifier == 1):
        infoY = e.y + 30
    else:
        infoY = e.y - 30
    chart.coords(info, infoX, infoY, infoX + 60, infoY + 20)
    chart.coords(infoLabel, infoX + 30, infoY + 10)
    for i in range(len(data)):
        rows[i].unover()
    if (identifier < len(data) - 1):
        rows[identifier].over()
        chart.itemconfig(infoLabel, text=data[identifier][0] + ": " + str(int(data[identifier][1]*10000)/100) + " %")
    
class Row():
    def __init__(self, nb, values):
        self.anim = 0
        self.char = values[0]
        self.percentage = values[1]
        self.x0 = 21
        self.x1 = self.x0
        self.y0 = 20 + nb * 15
        self.y1 = self.y0 + 13
        self.rect = chart.create_rectangle(self.x0, self.y0, self.x1, self.y1, fill="#4fade3" , outline="")
        self.label = chart.create_text(self.x0 - 10, self.y0 + 5, text=self.char, fill="#333333")

    def animate(self):
        global maxValue
        if (self.anim < 1):
            self.anim += 0.02
            self.x1 = self.x0 + (560 * (self.percentage/maxValue)) * self.anim
            chart.coords(self.rect, self.x0, self.y0, self.x1, self.y1)

    def over(self):
        chart.itemconfig(self.rect, fill="#95cdee")

    def unover(self):
        chart.itemconfig(self.rect, fill="#4fade3")


maxValue = 0.1

root = Tk()

menu = Menu(root)
root.config(menu=menu)

filemenu = Menu(menu)
menu.add_cascade(label="Fichier", menu=filemenu)
filemenu.add_command(label="Charger un texte", command=load)

titleLabel = Label(root, text="Merci de charger un texte à l'aide du menu ci dessus")
titleLabel.grid(row=0, column=0)

chart = Canvas(root, width=600, height=400, bg="white")
chart.grid(row=1, column=0)

root.mainloop()
