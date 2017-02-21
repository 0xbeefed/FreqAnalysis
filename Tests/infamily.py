def decodeFromFile(path):
    # Renvoie un tableau de données statistiques à partir d'un chemin de fichier path
    file = open(path, encoding='latin_1')
    data = file.readlines()
    file.close()

    # Creation d'un array exploitable
    for i in range(len(data)):
        # Chaque data[i] est de la forme 'nombre pourcentage\n' à cette etape
        data[i] = data[i].replace('\n', '').split()
        if (i != 0):
            data[i][0] = chr(int(data[i][0]))
            data[i][1] = int(data[i][1])
        
    # Creation des familles de lettres
    result = {'lenght': int(data[0][0]), 'ordering': [], 'other': [0.0]}
    families = [['e', 'eéèëê'], ['a', 'aàâä'], ['o', 'oôö'], ['chiffres', '0123456789+-*/='], ['n', 'nñ'], ['ponctuation', '{}[]_-\'"?.,;:!'], ['i', 'iîï'], ['u', 'uùûü']]
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
    
    return result

data = decodeFromFile("result.txt")
print(data)
