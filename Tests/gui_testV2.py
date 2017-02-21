from tkinter import *
from tkinter import filedialog
from math import *
import hashlib
import os

def decodeFromFile(path):
    # Renvoie un tableau de données statistiques à partir d'un chemin de fichier path
    file = open(path, encoding='latin_1')
    data = file.readlines()
    file.close()

    # Creation d'un array exploitable
    for i in range(len(data)):
        # Chaque data[i] est de la forme 'nombre occurences\n' à cette etape
        data[i] = data[i].replace('\n', '').split()
        if (i != 0):
            data[i][0] = chr(int(data[i][0]))
            data[i][1] = int(data[i][1])
        
    # Creation des familles de lettres
    result = {'lenght': int(data[0][0]), 'ordering': [], 'other': [0.0]}
    families = [['a', 'aâäà'], ['z', 'z'], ['e', 'eéèëê'], ['r', 'r'], ['t', 't'], ['y', 'yÿ'], ['u', 'uùûü'], ['i', 'iîï'], ['o', 'oôö'], ['p', 'p'],
                ['q', 'q'], ['s', 's'], ['d', 'd'], ['f', 'f'], ['g', 'g'], ['h', 'h'], ['j', 'j'], ['k', 'k'], ['l', 'l'], ['m', 'm'],
                ['w', 'w'], ['x', 'x'], ['c', 'cç'], ['v', 'v'], ['b', 'b'], ['n', 'nñ'],
                ['chif', '0123456789'], ['ponc', '"?.,;:!\'"']]
    for char in range(1, len(data)):
        inFamily = False
        for family in range(len(families)):
            if (families[family][1].find(data[char][0]) != -1):
                inFamily = True
                if (families[family][0] in result):
                    result[families[family][0]][0] = result[families[family][0]][0] + data[char][1]/result['lenght']
                    result[families[family][0]].append([data[char][0], data[char][1]/result['lenght']])
                else:
                    result['ordering'].append(families[family][0])
                    result[families[family][0]] = [data[char][1]/result['lenght'], [data[char][0], data[char][1]/result['lenght']]]
        if (not inFamily):
            result['other'][0] = result['other'][0] + data[char][1]/result['lenght']
            result['other'].append([data[char][0], data[char][1]/result['lenght']])
    result['ordering'].append('other')

    
    array = []
    for i in range(len(result['ordering'])):
        array.append([result[result['ordering'][i]][0], result['ordering'][i]])
    result['ordering'] = sorted(array, reverse=True)
    
    return result

def makeStats(path):
    # Creation du fichier statistique
    file = open(path, encoding='utf-8', mode='r')
    chain = file.read().lower()
    chainLen = len(chain)
    file.close()

    #generation
    dico = {}
    for letter in chain:
        dico[letter] = dico.get(letter, 0) + 1

    #sauvegarde
    saveTo = hashlib.md5()
    saveTo.update(path.encode('utf-8'))
    saveTo = "statistics/" + saveTo.hexdigest() + ".dat"
    output = str(chainLen) + '\n'
    for key in dico:
        if (key != " " and key != "\n"):
            output += str(ord(key)) + ' ' + str(dico[key]) + '\n'
    save = open(saveTo, mode='w')
    save.write(output)
    save.close()

    return saveTo

def displayStats(path):
    global data, rows, info, infoLabel, maxValue
    data = decodeFromFile(path)
    rows = []

    #Create interface
    chart.create_line(20, 0, 20, 600, fill="#555555")
    for i in range(1, ceil(560/80)):
        x = 21 + i * 80
        chart.create_line(x, 10, x, 600, fill="#888888")
        chart.create_text(x, 555, text=str(int((((x-21)/560)*maxValue)*10000)/100) + " %", fill="#333333")
        
    #Create rows
    for i in range(len(data['ordering'])):
        rows.append(Row(i-1, data['ordering'][i]))
        
    for e in range(50):
        for i in range(len(data['ordering'])):
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
    if (identifier < len(data)):
        rows[identifier].over()
        chart.itemconfig(infoLabel, text=data['ordering'][i][1] + ": " + str(int(data[data['ordering'][i][0]][0]*10000)/100) + " %")
    
class Row():
    def __init__(self, nb, char):
        global data
        self.anim = 0
        self.char = char[1]
        self.percentage = char[0]
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


maxValue = 0.2

root = Tk()

menu = Menu(root)
root.config(menu=menu)

filemenu = Menu(menu)
menu.add_cascade(label="Fichier", menu=filemenu)
filemenu.add_command(label="Charger un texte", command=load)

titleLabel = Label(root, text="Merci de charger un texte à l'aide du menu ci dessus")
titleLabel.grid(row=0, column=0)

chart = Canvas(root, width=600, height=600, bg="white")
chart.grid(row=1, column=0)

root.mainloop()
