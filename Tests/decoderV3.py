import time
start_time = time.time()

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
    families = [['a', 'aâäà'], ['z', 'z'], ['e', 'eéèëê'], ['r', 'r'], ['t', 't'], ['y', 'yÿ'], ['u', 'uùûü'], ['i', 'iîï'], ['o', 'oôö'], ['p', 'p'], ['q', 'q'], ['s', 's'], ['d', 'd'], ['f', 'f'], ['g', 'g'], ['h', 'h'], ['j', 'j'], ['k', 'k'], ['l', 'l'], ['m', 'm'], ['w', 'w'], ['x', 'x'], ['c', 'cç'], ['v', 'v'], ['b', 'b'], ['n', 'nñ'], ['chif', '0123456789'], ['ponc', '"?.,;:!\'"']]

    for char in range(1, len(data)):
        inFamily = False
        for family in range(len(families)):
            # Pour chaque famille
            if (families[family][1].find(data[char][0]) != -1):
                inFamily = True
                if (families[family][0] in result['chars']):
                    # Si la famille est déja crée, on la met à jour
                    result['chars'][families[family][0]][0] = result['chars'][families[family][0]][0] + data[char][1]/result['lenght']
                    result['chars'][families[family][0]].append([data[char][0], data[char][1]/result['lenght']])
                else:
                    # Sinon, on la crée
                    result['ordering'].append(families[family][0])
                    result['chars'][families[family][0]] = [data[char][1]/result['lenght'], [data[char][0], data[char][1]/result['lenght']]]
        if (not inFamily):
            # Si le caractere n'appartient à aucune famille, on le classe dans "autres"
            result['chars']['other'][0] = result['chars']['other'][0] + data[char][1]/result['lenght']
            result['chars']['other'].append([data[char][0], data[char][1]/result['lenght']])
            
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

data = decodeFromFile('result.txt')

print('Execution: ' + str(time.time() - start_time) + ' secondes ')

