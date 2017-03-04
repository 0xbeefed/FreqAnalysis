# Directives d'importations
import os
try:
    from tkinter import *      # module Tkinter pour Python 3
except:
    from Tkinter import *      # module Tkinter pour Python 2
from tkinter import filedialog

def drawFamily(char, data):
    """Fonction qui trace le diagramme circulaire."""
    chart.delete(ALL) # Efface le précédant diagramme circulaire (ne fait rien si il n'existe pas) afin de créer le nouveau.
    family = data['chars'][char]
    colors = []
    totalValue = family[0]
    startAngle = 0
    cache = []
    
    for i in range(1, len(family)):
        cache.append(family[i])
        
    items = sorted(cache, key=lambda x: x[1], reverse=True)
    colors = ['#' + str(hex(i)[2:].zfill(6)) for i in range(0, 16581375, int(16581375/len(family)))] # 16 581 375 correspond au nombre de couleurs differentes possibles pour les valeurs R, G et B entre 0 et 255.
    
    for i in range(len(items)):
        degrees = (items[i][1]/totalValue) * 360 # Calcul du poucentage de la famille que l'item représente.
        if (degrees > 0.1): # L'affichage d'un arc de moins de 0.1° provoque un bug graphique.
            chart.create_arc(20, 20, 280, 280, style='pieslice', start=startAngle, extent=degrees, outline='', fill=colors[i])
            chart.create_oval(90, 90, 210, 210, outline='', fill='#ffffff')
            startAngle += degrees
        if (int((items[i][1] / totalValue) * 100)) < 0.1:
            value = '< 0.1%'
        elif (int((items[i][1] / totalValue) * 100) == 100):
            chart.create_oval(20, 20, 280, 280, outline=outline, fill=color)
            chart.create_oval(90, 90, 210, 210, outline=outline, fill='#ffffff')
            value = '100%'
        else:
            value = str((int((items[i][1] / totalValue) * 100))) + '%'
        chart.create_text(150, 300 + i * 25, text=items[i][0] + ' : ' + value, fill=colors[i], font=('Arial', 14))
        
    if int(totalValue * 100) < 1:
        value = "< 1%"
    else:
        value = str(int(totalValue * 100)) + "%"
    chart.create_text(150, 150, text=char + ' :\n' + value, fill='#333333', font=('Arial', 26), justify=CENTER) # Affiche la famille de caractères survolée et son pourcentage dans le texte.

def decodeFromFile(path):
    """Fonction qui retourne la fréquence de chaque caractère du fichier texte à l'emplacement "path" dans un dictionnaire."""
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
    families = [['a', 'aâäà'], ['z', 'z'], ['e', 'eéèëê'], ['r', 'r'], ['t', 't'], ['y', 'yÿ'], ['u', 'uùûü'], ['i', 'iîï'], ['o', 'oôö'], ['p', 'p'], ['q', 'q'], ['s', 's'], ['d', 'd'], ['f', 'f'], ['g', 'g'], ['h', 'h'],
                ['j', 'j'], ['k', 'k'], ['l', 'l'], ['m', 'm'], ['w', 'w'], ['x', 'x'], ['c', 'cç'], ['v', 'v'], ['b', 'b'], ['n', 'nñ'], ['chif', '0123456789'], ['ponc', '"?.,;:!\'"']]

    for char in dico:
        inFamily = False
        for family in range(len(families)):
            # Pour chaque famille...
            if (families[family][1].find(char) != -1):
                inFamily = True
                if (families[family][0] in result['chars']):
                    # ...si la famille est déja crée, on la met à jour...
                    result['chars'][families[family][0]][0] = result['chars'][families[family][0]][0] + dico[char]/result['lenght']
                    result['chars'][families[family][0]].append([char, dico[char]/result['lenght']])
                else:
                    # ...sinon, on la crée.
                    result['ordering'].append(families[family][0])
                    result['chars'][families[family][0]] = [dico[char]/result['lenght'], [char, dico[char]/result['lenght']]]
        if (not inFamily):
            # Si le caractère n'appartient à aucune famille, on le classe dans "autres".
            result['chars']['other'][0] = result['chars']['other'][0] + dico[char]/result['lenght']
            result['chars']['other'].append([char, dico[char]/result['lenght']])
                
    if (result['chars']['other'][0] != 0.0):
        # Si la liste "autre" n'est pas vide, on l'ajoute à la liste des colonnes à afficher.
        result['ordering'].append('other')

    # Classement du dictionnaire par pourcentage décroissant.
    array = []
    for i in range(len(result['ordering'])):
        array.append([result['chars'][result['ordering'][i]][0], result['ordering'][i]])
    result['ordering'] = sorted(array, reverse=True)
    for i in range(len(result['ordering'])):
        result['ordering'][i] = result['ordering'][i][1]
        
    return result

def load():
    """Fonction qui crée une fenêtre de dialogue et appelle les fonctions "decodeFromFile" et "createGraph"."""
    path = filedialog.askopenfilename(initialdir=os.getcwd() + "/librairie/", title="Analyse frequencielle", filetypes=[('Text Files', "*.txt")])
    if (path != ""):
        titleLabel.config(text=path)
        data = decodeFromFile(path)
        createGraph(data)

def motion(event):
    """Fonction qui gère les modifications des diagrammes en fonction de la position du curseur."""
    x, y = event.x, event.y # Récupère les positions x et y du curseur.
    for i in range(len(parameterList)):
        if parameterList[i][2] < x and x < parameterList[i][4]: # Si le curseur est entre les parametres x0 et x1 d'une colonne...
            columnList[i].above() # ...effectue la fonction "above" de cette colonne...
        else:
            columnList[i].notAbove() # ...sinon effectue la fonction "notAbove" de cette colonne.

def createGraph(data):
    """Fonction qui trace le diagramme en bâtons."""
    global parameterList, columnList
    parameterList = []
    columnList = []
    canvas.delete(ALL) # Efface le précédant diagramme en bâtons (ne fait rien si il n'existe pas) afin de créer le nouveau.
    
    occurenceMax = int(data['chars'][data['ordering'][0]][0] * 100) # Récupère la plus grand valeur à afficher.

    maxLineIndex = int(occurenceMax + (5 - occurenceMax % 5)) # Donne la valeur multiple de 5 supérieur la plus proche de occurenceMax (pour les lignes horizontales).
    totalLength = len(data['ordering']) # Calcul du nombre total de colonne à afficher, 1 par famille de caractère.
    sizeCaracter = (width - 40) // totalLength # Calcul de la largeur de l'espace correspondant a chaque caractère.
    sizeBetweenLine = (height - 40) // (maxLineIndex // 5) # Calcul la distance entre chaque lignes horizontales.
    
    for i in range(maxLineIndex // 5 + 1): # Trace les lignes horizontales et leurs valeurs, trace 1 ligne supplémentaire au dessus de la valeur max.
        x0 = 20
        y0 = 20 + i * sizeBetweenLine
        x1 = 20 + sizeCaracter * totalLength
        y1 = 20 + i * sizeBetweenLine
        canvas.create_line(x0, y0, x1, y1)
        canvas.create_text(10, 20 + i * sizeBetweenLine, text = str(maxLineIndex - (i * 5)))

    for i in range(totalLength + 1): # Trace les petites lignes verticales qui délimitent les espaces pour chaque famille de caractère, comme il y a 1 ligne de plus que de caractère on crée n + 1 lignes avec n le nombre de caractère.
        x0 = 20 + i*sizeCaracter
        y0 = 20 + sizeBetweenLine * (maxLineIndex // 5)
        x1 = 20 + i*sizeCaracter
        y1 = 20 + sizeBetweenLine * (maxLineIndex // 5) + 10
        canvas.create_line(x0, y0, x1, y1)
        
    for i in range(totalLength): # Trace les caractères entre chaque petites lignes verticales.
        x0 = 20 + i * sizeCaracter + sizeCaracter // 2
        y0 = 30 + sizeBetweenLine * (maxLineIndex // 5)
        canvas.create_text(x0, y0, text = data['ordering'][i])
        
    for i in range(totalLength): # Enregistre les positions x0, y0, x1 et y1 de chaque colonne.
        char = data['ordering'][i]
        percentage = data['chars'][char][0]
        x0 = int(20 + sizeCaracter // 4 + i * sizeCaracter)
        y0 = int(20 + sizeBetweenLine * (maxLineIndex // 5))
        x1 = int(20 + sizeCaracter // 4 + i * sizeCaracter + sizeCaracter // 2)
        y1 = int(20 + sizeBetweenLine * maxLineIndex // 5 - percentage * 20 * sizeBetweenLine)
        parameterList.append([char, percentage, x0, y0, x1, y1])
        
    for i in range(len(parameterList)):
        columnList.append(Rectangle(parameterList[i][0], parameterList[i][1], parameterList[i][2], parameterList[i][3], parameterList[i][4], parameterList[i][5], data)) # Affecte une colonne a chaque index de columnList.
        
    for state in range(20):
        for i in range(len(columnList)):
            columnList[i].animate()
        canvas.update()

class Rectangle:
    """La classe Rectangle regroupe les attributs de chaque colonne. Cette classe comprend les méthodes : __init__, animate, above et notAbove."""
    def __init__(self, character, percentage, x0, y0, x1, y1, data):
        """
        Méthode constructeur de la classe Rectangle.

        Prend en paramètre:
            -le caractère correspondant à ce rectangle ainsi que son pourcentage, 
            -les positions x0, x1, y0 et y1 du rectangle que l'on veut tracer,
            -la liste data contenant toutes les informations sur les caractères.
            
        """
        self.char = character
        self.percentage = percentage
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y0 # Le recantgle est plat avant le début de l'animation.
        self.goal = y0 - y1
        self.column = canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1, fill=color, outline=outline)
        self.state = 0
        self.data = data
        
    def animate(self):
        """Méthode de la classe Rectangle. Réalise l'animation de l'apparition du rectangle. A chaque appel, augmente de 5% la surface de rectangle à afficher puis l'affiche."""
        self.state += 0.05
        self.y1 = self.y0 - (self.goal * self.state)
        canvas.coords(self.column, self.x0, self.y0, self.x1, self.y1 + 1) # self.y1 + 1 car le contour du rectangle fais 1px et n'est pas prit en compte dans sa taille.

    def above(self):
        """Méthode de la classe Rectangle. Change la couleur du rectangle sur lequel est le curseur et appelle la fonction "drawFamily". Méthode appellée quand le curseur se trouve sur ce rectangle."""
        canvas.itemconfig(self.column, fill='#2f6788', state=NORMAL)
        drawFamily(self.char, self.data)
        
    def notAbove(self):
        """Méthode de la classe Rectangle. Donne la couleur initiale au rectangle. Méthode appellée quand le curseur ne se trouve pas sur ce rectangle."""
        canvas.itemconfig(self.column, fill=color)

outline = '#275671'
color = '#4fade3'
     
root = Tk()
root.state('zoomed')# 'zoomed' correspond au mode plein écran.
parameterList = []
columnList = []
menu = Menu(root)
root.config(menu=menu)

filemenu = Menu(menu)
menu.add_cascade(label="Fichier", menu=filemenu)
filemenu.add_command(label="Charger un texte", command=load)

titleLabel = Label(root, text="Merci de charger un texte à l'aide du menu ci dessus")
titleLabel.grid(row=0, column=0)

height = root.winfo_screenheight() - 110 
width = root.winfo_screenwidth() - 300 # On laisse 300px de disponibles pour la création du diagramme circulaire.

graphLabel = Label(root)
graphLabel.grid(row=1, column=0)

canvas = Canvas(graphLabel, width=width, height=height, bg='#ffffff') # Diagramme en bâtons.
canvas.grid(row=0, column=0)

chart = Canvas(graphLabel, width=300, height=height, bg='#ffffff') # Diagramme circulaire.
chart.grid(row=0, column=1)

root.bind('<Motion>', motion) # Effectue la fonction "motion" quand il y a un mouvement du curseur.

root.mainloop()
