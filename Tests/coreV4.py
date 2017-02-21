import time
start_time = time.time()

#ouverture
file = open('librairie/Origine_Des_Especes.txt', encoding='utf-8', mode='r')
chain = file.read().lower()
chainLen = len(chain)
file.close()

#generation
dico = {}
for letter in chain:
    dico[letter] = dico.get(letter, 0) + 1

#sauvegarde
output = str(chainLen) + '\n'
for key in dico:
    if (key != " " and key != "\n"):
        output += str(ord(key)) + ' ' + str(dico[key]) + '\n'
save = open('result.txt', mode='w')
save.write(output)
save.close()

print('Execution: ' + str(time.time() - start_time) + ' secondes pour ' + str(chainLen) + ' caractères')


