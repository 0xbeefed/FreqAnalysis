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

data = decodeFromFile('librairie/Genese_Ancien_testament.txt')

print(data)
