# parseur json maison
# on lit la reponse du serveur sans utiliser le module json

def lire_json(texte):
    texte = texte.strip()
    i = 0

    def sauter_espaces():
        nonlocal i
        while i < len(texte) and texte[i] in ' \t\n\r':
            i += 1

    def lire_valeur():
        nonlocal i
        sauter_espaces()
        c = texte[i]
        if c == '{':
            return lire_objet()
        if c == '[':
            return lire_liste()
        if c == '"':
            return lire_chaine()
        if texte[i:i+4] == 'true':
            i += 4
            return True
        if texte[i:i+5] == 'false':
            i += 5
            return False
        if texte[i:i+4] == 'null':
            i += 4
            return None
        return lire_nombre()

    # on lit une chaine entre guillemets
    def lire_chaine():
        nonlocal i
        i += 1
        res = ""
        while texte[i] != '"':
            if texte[i] == '\\':
                i += 1
                suivant = texte[i]
                if suivant == 'n':
                    res += '\n'
                elif suivant == 't':
                    res += '\t'
                else:
                    res += suivant
            else:
                res += texte[i]
            i += 1
        i += 1
        return res

    # on lit un nombre entier ou decimal
    def lire_nombre():
        nonlocal i
        debut = i
        while i < len(texte) and texte[i] in '-+.0123456789eE':
            i += 1
        morceau = texte[debut:i]
        if '.' in morceau or 'e' in morceau or 'E' in morceau:
            return float(morceau)
        return int(morceau)

    # on lit un objet entre accolades
    def lire_objet():
        nonlocal i
        i += 1
        obj = {}
        sauter_espaces()
        if texte[i] == '}':
            i += 1
            return obj
        while True:
            sauter_espaces()
            cle = lire_chaine()
            sauter_espaces()
            i += 1
            obj[cle] = lire_valeur()
            sauter_espaces()
            if texte[i] == ',':
                i += 1
            else:
                i += 1
                break
        return obj

    # on lit une liste entre crochets
    def lire_liste():
        nonlocal i
        i += 1
        liste = []
        sauter_espaces()
        if texte[i] == ']':
            i += 1
            return liste
        while True:
            liste.append(lire_valeur())
            sauter_espaces()
            if texte[i] == ',':
                i += 1
            else:
                i += 1
                break
        return liste

    return lire_valeur()
