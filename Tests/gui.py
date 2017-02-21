from tkinter import *
from tkinter import filedialog
from math import *
import hashlib
import os
import time

def decodeFromFile(path):
    # Renvoie un tableau de données statistiques à partir d'un chemin de fichier path
    # result[chars | ordering | lenght]
    file = open(path, encoding='utf-8')
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
    result = {'lenght': int(data[0][0]), 'ordering': [], 'chars': {'other': [0.0]}}
    families = [['a', 'aâäà'], ['z', 'z'], ['e', 'eéèëê'], ['r', 'r'], ['t', 't'], ['y', 'yÿ'], ['u', 'uùûü'], ['i', 'iîï'], ['o', 'oôö'], ['p', 'p'],
                ['q', 'q'], ['s', 's'], ['d', 'd'], ['f', 'f'], ['g', 'g'], ['h', 'h'], ['j', 'j'], ['k', 'k'], ['l', 'l'], ['m', 'm'],
                ['w', 'w'], ['x', 'x'], ['c', 'cç'], ['v', 'v'], ['b', 'b'], ['n', 'nñ'],
                ['chif', '0123456789'], ['ponc', '"?.,;:!\'"']]
    for char in range(1, len(data)):
        inFamily = False
        for family in range(len(families)):
            if (families[family][1].find(data[char][0]) != -1):
                inFamily = True
                if (families[family][0] in result['chars']):
                    result['chars'][families[family][0]][0] = result['chars'][families[family][0]][0] + data[char][1]/result['lenght']
                    result['chars'][families[family][0]].append([data[char][0], data[char][1]/result['lenght']])
                else:
                    result['ordering'].append(families[family][0])
                    result['chars'][families[family][0]] = [data[char][1]/result['lenght'], [data[char][0], data[char][1]/result['lenght']]]
        if (not inFamily):
            result['chars']['other'][0] = result['chars']['other'][0] + data[char][1]/result['lenght']
            result['chars']['other'].append([data[char][0], data[char][1]/result['lenght']])
    if (result['chars']['other'][0] != 0.0):
        result['ordering'].append('other')

    # Classement du dictionnaire par pourcentage decroissant
    array = []
    for i in range(len(result['ordering'])):
        array.append([result['chars'][result['ordering'][i]][0], result['ordering'][i]])
    result['ordering'] = sorted(array, reverse=True)
    for i in range(len(result['ordering'])):
        result['ordering'][i] = result['ordering'][i][1]
    
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


def load():
    path = filedialog.askopenfilename(initialdir=os.getcwd() + "/librairie/", title="Analyse frequencielle", filetypes=[("Text Files", "*.txt")])
    if (path != ""):
        titleLabel.config(text=path)
        generated = makeStats(path)
        data = decodeFromFile(path)
        createGraph(data)
    else:
        print("aborted")


def motion(event):
    x, y = event.x, event.y #position du curseur
    #print('{}, {}'.format(x, y))
    for i in range(len(parameterList)):
        if parameterList[i][2] < x and x < parameterList[i][4]: #and parameterList[i][3] > y and y > parameterList[i][5]: <- a ajouter pour que le survolaj se fasse uniquement sur le rectangle et pas toute la colonne
            charText.config(text = "caractere : " + parameterList[i][0])
            percentageText.config(text = "pourcentage : " + str(round(parameterList[i][1] * 100, 2)) + " %")
            columnList[i].above(x, y)
        else:
            columnList[i].notAbove()

def createGraph(data):
    
    global parameterList, columnList
        

    occurenceMax = int(data["chars"][data["ordering"][0]][0]*100)#recupere la plus grand valeur a afficher

    maxLineIndex = int(occurenceMax + (5 - occurenceMax%5)) #donne la valeur multiple de 5 superieur la plus proche de occurenceMax, pour les lignes horizontales
    totalLength = len(data["ordering"]) #nombre total de colonne
    sizeCaracter = (width - 40)//totalLength #largeur pour chaque caractere
    sizeBetweenLine = (height - 40)//(maxLineIndex//5)#distance entre chaque lignes horizontales

    textLabel.grid(row = 2, column = 0)
    charText.config(text = "Caractère : ")
    charText.grid(row = 0, column = 0)
    percentageText.config(text = "Pourcentage : ")
    percentageText.grid(row = 1, column = 0)

    for i in range(maxLineIndex//5 + 1): #lignes horizontales + valeurs
        x0 = 20
        y0 = 20 + i*sizeBetweenLine
        x1 = 20 + sizeCaracter*totalLength
        y1 = 20 + i*sizeBetweenLine
        canvas.create_line(x0, y0, x1, y1)
        canvas.create_text(10, 20 + i*sizeBetweenLine, text = str(maxLineIndex - (i*5)))

    for i in range(totalLength + 1): #petites lignes verticales, +1 car il y a une ligne de plus que de caractere
        x0 = 20 + i*sizeCaracter
        y0 = 20 + sizeBetweenLine*(maxLineIndex//5)
        x1 = 20 + i*sizeCaracter
        y1 = 20 + sizeBetweenLine*(maxLineIndex//5) + 10
        canvas.create_line(x0, y0, x1, y1)
        
    for i in range(totalLength): #caractere
        x0 = 20 + i*sizeCaracter + sizeCaracter//2
        y0 = 30 + sizeBetweenLine*(maxLineIndex//5)
        canvas.create_text(x0, y0, text = data["ordering"][i])
        
    for i in range(totalLength):#enregistre les positions x0, y0, x1 et y1 de chaque colonne
        char = data["ordering"][i]
        percentage = data["chars"][char][0]
        x0 = int(20 + sizeCaracter//4 + i*sizeCaracter)
        y0 = int(20 + sizeBetweenLine*(maxLineIndex//5))
        x1 = int(20 + sizeCaracter//4 + i*sizeCaracter + sizeCaracter//2)
        y1 = int(20 + sizeBetweenLine*maxLineIndex//5 - percentage*20*sizeBetweenLine)
        parameterList.append([char, percentage, x0, y0, x1, y1])
        
    for i in range(len(parameterList)):
        columnList.append(Rectangle(parameterList[i][0], parameterList[i][1], parameterList[i][2], parameterList[i][3], parameterList[i][4], parameterList[i][5]))#affecte une colonne a chaque index


class Rectangle:
    def __init__(self, character, percentage, x0, y0, x1, y1):
        self.char = character
        self.percentage = percentage
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.createRectangle()
        #self.popUp = canvas.create_rectangle(0,0,0,0)
        
    def createRectangle(self):
        #print(str(self.x0) + " " + str(self.y0) + " " + str(self.x1) + " " + str(self.y1))
        self.column = canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1, fill = color)
        timeAnim = int(self.y0 - self.y1)//20 # > 120 : accelere / < 120 : ralentit
        for i in range(1,timeAnim + 1): #de 1 a timeAnim + 1 sinon ZeroDivisionError       
            canvas.coords(self.column, self.x0, self.y0, self.x1, self.y0 - (self.y0 - self.y1)*i/(timeAnim))
            time.sleep(0.001)
            root.update()

    def above(self, x, y):
        canvas.itemconfig(self.column, fill = "green", state = NORMAL)
        #self.popUp = canvas.create_rectangle(x, y, x + 50, y + 20, fill = "red")
        
    def notAbove(self):
        canvas.itemconfig(self.column, fill = "#4fade3")
        #canvas.delete(self.popUp)

color = "#4fade3"

#decodeFromFile("result.txt")
#data = {'ordering': ['e', 's', 'a', 'n', 'i', 't', 'r', 'l', 'u', 'o', 'ponc', 'd', 'c', 'p', 'm', 'q', 'chif', 'v', 'other', 'g', 'b', 'f', 'h', 'x', 'y', 'j', 'w', 'k', 'z'], 'chars': {'other': [0.008642212406376032, ['[', 0.00019204916458613405], ['-', 0.0016324178989821393], ['«', 0.0005761474937584022], ['(', 0.0010562704052237374], [')', 0.0010562704052237374], ['_', 0.0032648357979642786], ['»', 0.0005761474937584022], ['§', 9.602458229306702e-05], [']', 0.00019204916458613405]], 'y': [0.0021125408104474747, ['y', 0.0021125408104474747]], 'm': [0.023814096408680624, ['m', 0.023814096408680624]], 'o': [0.039562127904743616, ['ô', 9.602458229306702e-05], ['o', 0.03946610332245055]], 'v': [0.0090263107355483, ['v', 0.0090263107355483]], 'n': [0.057422700211254084, ['n', 0.057422700211254084]], 'z': [0.0003840983291722681, ['z', 0.0003840983291722681]], 'd': [0.028903399270213175, ['d', 0.028903399270213175]], 'i': [0.055502208565392744, ['î', 0.0002880737468792011], ['i', 0.05521413481851354]], 'l': [0.0442673324371039, ['l', 0.0442673324371039]], 'r': [0.050412905703860186, ['r', 0.050412905703860186]], 'ponc': [0.031496062992125984, ['.', 0.006817745342807759], [':', 0.00019204916458613405], ["'", 0.009506433647013635], [';', 0.0011522949875168043], [',', 0.013731515267908584], ['?', 9.602458229306702e-05]], 't': [0.05511811023622047, ['t', 0.05511811023622047]], 'j': [0.0019204916458613404, ['j', 0.0019204916458613404]], 'chif': [0.010178605723065105, ['5', 0.0007681966583445362], ['6', 0.0003840983291722681], ['8', 0.0017284424812752065], ['0', 0.0006721720760514692], ['2', 0.0006721720760514692], ['1', 0.002688688304205877], ['9', 0.0009602458229306702], ['4', 0.0006721720760514692], ['3', 0.0008642212406376032], ['7', 0.0007681966583445362]], 'q': [0.010850777799116574, ['q', 0.010850777799116574]], 'e': [0.1429806030343768, ['é', 0.016708277318993662], ['è', 0.004897253696946418], ['ê', 0.0014403687343960054], ['e', 0.11993470328404071]], 'u': [0.04388323410793163, ['ù', 9.602458229306702e-05], ['û', 0.0003840983291722681], ['u', 0.043403111196466296]], 'b': [0.007393892836566161, ['b', 0.007393892836566161]], 'x': [0.003168811215671212, ['x', 0.003168811215671212]], 'a': [0.061359708085269825, ['à', 0.003648934127136547], ['a', 0.05761474937584021], ['â', 9.602458229306702e-05]], 's': [0.07259458421355867, ['s', 0.07259458421355867]], 'k': [0.0005761474937584022, ['k', 0.0005761474937584022]], 'w': [0.0012483195698098713, ['w', 0.0012483195698098713]], 'c': [0.028807374687920106, ['ç', 0.0002880737468792011], ['c', 0.028519300941040906]], 'f': [0.007009794507393893, ['f', 0.007009794507393893]], 'g': [0.007489917418859228, ['g', 0.007489917418859228]], 'h': [0.0056654503552909545, ['h', 0.0056654503552909545]], 'p': [0.028039178029575573, ['p', 0.028039178029575573]]}, 'lenght': 10414}
#data = decodeFromFile("result.txt")

parameterList = []
columnList = []

root = Tk()
root.state('zoomed')# == fullscreen
parameterList = []
columnList = []
menu = Menu(root)
root.config(menu=menu)


textLabel = Label(root)
charText = Label(textLabel)
percentageText = Label(textLabel)


filemenu = Menu(menu)
menu.add_cascade(label="Fichier", menu=filemenu)
filemenu.add_command(label="Charger un texte", command=load)

titleLabel = Label(root, text="Merci de charger un texte à l'aide du menu ci dessus")
titleLabel.grid(row=0, column=0)

height = root.winfo_screenheight()//1.2 #Si reduit pas la hauteur la barre de tache gene le bas de la fenetre
width = root.winfo_screenwidth()

canvas = Canvas(height = height, width = width, bg = "white")#futur graph
canvas.grid(row = 1, column = 0)

root.bind("<Motion>", motion)#effectue la fonction "motion" quand il y a un mouvement du curseur

root.mainloop()
