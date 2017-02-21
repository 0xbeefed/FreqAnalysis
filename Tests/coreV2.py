import time
import os
start_time = time.time()

#ouverture
file = open("file.txt", encoding="latin_1")
chain = file.read().lower()
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
output = str(chainLen) + "\n"
for key in dico:
    output += key + " " + str(dico[key]/chainLen) + "\n"
save = open("result.txt", mode="w")
save.write(output)
save.close()

print("Execution: " + str(time.time() - start_time) + " secondes pour " + str(len(chain)) + " caractères")
