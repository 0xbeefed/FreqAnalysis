try:
    from tkinter import *      # module Tkinter pour Python 3
except:
    from Tkinter import *      # module Tkinter pour Python 2
from tkinter import filedialog
import os

def drawFamily(char, data):
    chart.delete(ALL)
    family = data['chars'][char]
    colors = []
    totalValue = family[0]
    startAngle = 0
    if int(totalValue * 100) < 1:
        value = "< 1%"
    else:
        value = str(int(totalValue * 100)) + "%"
    chart.create_text(150, 30, text=char + ' : ' + value, fill='#333333', font = ("Arial", 36, "underline"))
    cache = [];
    for i in range(1, len(family)):
        cache.append(family[i])
    items = sorted(cache, key=lambda x: x[1], reverse=True)
    colors = ['#' + str(hex(i)[2:].zfill(6)) for i in range(0, 16581375, int(16581375/len(family)))]
    
    for i in range(len(items)):

        degrees = (items[i][1]/totalValue) * 360 # calcul du poucentage de la famille que l'item represente
        if (degrees > 0.1): # l'affichage d'un arc de moins de 0.1° provoque un bug graphique
            chart.create_arc(20, 100, 280, 360, style='pieslice', start=startAngle, extent=degrees, outline='', fill=colors[i])
            startAngle += degrees
        if (int((items[i][1]/totalValue) * 100)) < 0.1:
            value = '< 0.1%'
        elif (int((items[i][1]/totalValue) * 100) == 100):
            chart.create_oval(20, 100, 280, 360, outline= outline, fill= color)
            value = '100%'
        else:
            value = str((int((items[i][1]/totalValue) * 100))) + '%'
        chart.create_text(150, 400 + i * 25, text=items[i][0] + ' : ' + value, fill=colors[i], font = ("Arial", 14))

def decodeFromFile(path):
    # Ouverture
    file = open(path, encoding='utf-8', mode='r')
    chain = file.read().lower()
    chainLen = len(chain)
    file.close()

    # Generation frequences
    dico = {}
    for letter in chain:
        if (letter != " " and letter != "\n"):
            dico[letter] = dico.get(letter, 0) + 1
        else:
            chainLen -= 1

    # Creation resultats
    result = {'lenght': chainLen, 'ordering': [], 'chars': {'other': [0.0]}}
    families = [['a', 'aâäà'], ['z', 'z'], ['e', 'eéèëê'], ['r', 'r'], ['t', 't'], ['y', 'yÿ'], ['u', 'uùûü'], ['i', 'iîï'], ['o', 'oôö'], ['p', 'p'], ['q', 'q'], ['s', 's'], ['d', 'd'], ['f', 'f'], ['g', 'g'], ['h', 'h'], ['j', 'j'], ['k', 'k'], ['l', 'l'], ['m', 'm'], ['w', 'w'], ['x', 'x'], ['c', 'cç'], ['v', 'v'], ['b', 'b'], ['n', 'nñ'], ['chif', '0123456789'], ['ponc', '"?.,;:!\'"']]

    for char in dico:
        inFamily = False
        for family in range(len(families)):
            # Pour chaque famille
            if (families[family][1].find(char) != -1):
                inFamily = True
                if (families[family][0] in result['chars']):
                    # Si la famille est déja crée, on la met à jour
                    result['chars'][families[family][0]][0] = result['chars'][families[family][0]][0] + dico[char]/result['lenght']
                    result['chars'][families[family][0]].append([char, dico[char]/result['lenght']])
                else:
                    # Sinon, on la crée
                    result['ordering'].append(families[family][0])
                    result['chars'][families[family][0]] = [dico[char]/result['lenght'], [char, dico[char]/result['lenght']]]
        if (not inFamily):
            # Si le caractere n'appartient à aucune famille, on le classe dans "autres"
            result['chars']['other'][0] = result['chars']['other'][0] + dico[char]/result['lenght']
            result['chars']['other'].append([char, dico[char]/result['lenght']])
                
    if (result['chars']['other'][0] != 0.0):
        # Si la liste "autre" n'est pas vide, on l'ajoute à la liste des colonnes a afficher
        result['ordering'].append('other')

    # Classement du dictionnaire par pourcentage decroissant
    array = []
    for i in range(len(result['ordering'])):
        array.append([result['chars'][result['ordering'][i]][0], result['ordering'][i]])
    result['ordering'] = sorted(array, reverse=True)
    for i in range(len(result['ordering'])):
        result['ordering'][i] = result['ordering'][i][1]

    return result

def load():
    path = filedialog.askopenfilename(initialdir=os.getcwd() + "/librairie/", title="Analyse frequencielle", filetypes=[("Text Files", "*.txt")])
    if (path != ""):
        titleLabel.config(text=path)
        data = decodeFromFile(path)
        createGraph(data)

def motion(event):
    x, y = event.x, event.y #position du curseur
    for i in range(len(parameterList)):
        if parameterList[i][2] < x and x < parameterList[i][4]: #and parameterList[i][3] > y and y > parameterList[i][5]: <- a ajouter pour que le survolaj se fasse uniquement sur le rectangle et pas toute la colonne
            columnList[i].above(x, y)
        else:
            columnList[i].notAbove()

def createGraph(data):
    global parameterList, columnList
    parameterList = []
    columnList = []
    canvas.delete(ALL)
    
    occurenceMax = int(data["chars"][data["ordering"][0]][0]*100)#recupere la plus grand valeur a afficher

    maxLineIndex = int(occurenceMax + (5 - occurenceMax%5)) #donne la valeur multiple de 5 superieur la plus proche de occurenceMax, pour les lignes horizontales
    totalLength = len(data["ordering"]) #nombre total de colonne
    sizeCaracter = (width - 40)//totalLength #largeur pour chaque caractere
    sizeBetweenLine = (height - 40)//(maxLineIndex//5)#distance entre chaque lignes horizontales
    
    for i in range(maxLineIndex//5 + 1): #lignes horizontales + valeurs
        x0 = 20
        y0 = 20 + i*sizeBetweenLine
        x1 = 20 + sizeCaracter*totalLength
        y1 = 20 + i*sizeBetweenLine
        canvas.create_line(x0, y0, x1, y1)
        canvas.create_text(10, 20 + i*sizeBetweenLine, text = str(maxLineIndex - (i*5)))

    for i in range(totalLength + 1): # petites lignes verticales, +1 car il y a une ligne de plus que de caractere
        x0 = 20 + i*sizeCaracter
        y0 = 20 + sizeBetweenLine*(maxLineIndex//5)
        x1 = 20 + i*sizeCaracter
        y1 = 20 + sizeBetweenLine*(maxLineIndex//5) + 10
        canvas.create_line(x0, y0, x1, y1)
        
    for i in range(totalLength): # caractere
        x0 = 20 + i*sizeCaracter + sizeCaracter//2
        y0 = 30 + sizeBetweenLine*(maxLineIndex//5)
        canvas.create_text(x0, y0, text = data["ordering"][i])
        
    for i in range(totalLength):# enregistre les positions x0, y0, x1 et y1 de chaque colonne
        char = data["ordering"][i]
        percentage = data["chars"][char][0]
        x0 = int(20 + sizeCaracter//4 + i*sizeCaracter)
        y0 = int(20 + sizeBetweenLine*(maxLineIndex//5))
        x1 = int(20 + sizeCaracter//4 + i*sizeCaracter + sizeCaracter//2)
        y1 = int(20 + sizeBetweenLine*maxLineIndex//5 - percentage*20*sizeBetweenLine)
        parameterList.append([char, percentage, x0, y0, x1, y1])
        
    for i in range(len(parameterList)):
        columnList.append(Rectangle(parameterList[i][0], parameterList[i][1], parameterList[i][2], parameterList[i][3], parameterList[i][4], parameterList[i][5], data))#affecte une colonne a chaque index
        
    for state in range(20):
        for i in range(len(parameterList)):
            columnList[i].animate()
        canvas.update()

class Rectangle:
    def __init__(self, character, percentage, x0, y0, x1, y1, data):
        self.char = character
        self.percentage = percentage
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y0
        self.goal = y0 - y1
        self.column = canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1, fill= color, outline = outline)
        self.state = 0
        self.data = data
        
    def animate(self):
        self.state += 0.05
        self.y1 = self.y0 - (self.goal * self.state)
        canvas.coords(self.column, self.x0, self.y0, self.x1, self.y1)

    def above(self, x, y):
        canvas.itemconfig(self.column, fill = "#2f6788", state = NORMAL)
        drawFamily(self.char, self.data)
        
    def notAbove(self):
        canvas.itemconfig(self.column, fill = color)

outline = "#275671"
color = "#4fade3"
     
root = Tk()
root.state('zoomed')# == fullscreen
parameterList = []
columnList = []
menu = Menu(root)
root.config(menu=menu)

filemenu = Menu(menu)
menu.add_cascade(label="Fichier", menu=filemenu)
filemenu.add_command(label="Charger un texte", command=load)

titleLabel = Label(root, text="Merci de charger un texte à l'aide du menu ci dessus")
titleLabel.grid(row=0, column=0)

height = root.winfo_screenheight()-110 #Si reduit pas la hauteur la barre de tache gene le bas de la fenetre
width = root.winfo_screenwidth()-300

graphLabel = Label(root)
graphLabel.grid(row = 1, column = 0)

canvas = Canvas(graphLabel, width=width, height=height, bg="#ffffff")#futur graph
canvas.grid(row = 0, column = 0)

chart = Canvas(graphLabel, width=300, height=height, bg='#ffffff')
chart.grid(row = 0, column = 1)

root.bind("<Motion>", motion)#effectue la fonction "motion" quand il y a un mouvement du curseur

root.mainloop()
