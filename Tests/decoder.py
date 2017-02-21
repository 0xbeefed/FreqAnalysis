def decodeFromFile(path):
    # Renvoie un tableau de données statistiques à partir d'un chemin de fichier path
    file = open(path, encoding='latin_1')
    data = file.readlines()
    file.close()
    for i in range(1, len(data)):
        # Chaque data[i] est de la forme 'nombre pourcentage\n' à cette etape
        data[i] = data[i].replace('\n', '').split()
        data[i][0] = chr(int(data[i][0]))
        data[i][1] = float(data[i][1])
    #lenght = int(data[0][0])
    data = sorted(data[1:], key=lambda x: x[1], reverse=True)
    return data

print(decodeFromFile('result.txt'))
