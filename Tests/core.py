import time
start_time = time.time()

def inDico(dico, char):
    # Retourne -1 si le char n'est pas présent dans le dictionnaire dico et son index dans ce tableau si il est présent
    result = False
    for i in range(len(dico)):
        if (dico[i][0] == char):
            result = i
    return result

# file un fichier de type texte a traiter
file = open("file.txt", encoding="latin_1")
chain = file.read().lower()
file.close()
dico = []

# generation du tableau de frequence
for i in range(len(chain)):
    inDicoValue = inDico(dico, chain[i])
    if (not inDicoValue and chain[i] != "\n" and chain[i] != " "):
        dico.append([chain[i], 1])
    else:
        dico[inDicoValue][1] += 1

# tri du tableau par frequence d'appartition
dico = sorted(dico, key=lambda x: x[1], reverse=True)

# enregistrement du resultat sous un format texte
output = open("result.txt", mode="w")
toWrite = str(len(chain)) + "\n"
for i in range(len(dico)):
  toWrite += str(dico[i][0]) + " " + str(dico[i][1]/len(chain)) + "\n"
output.write(toWrite)
output.close()

print("--- %s seconds ---" % (time.time() - start_time))
