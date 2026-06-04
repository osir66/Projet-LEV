import math

def cartesien_vers_polaire(x, y):
    r = math.hypot(x, y)
    theta = math.atan2(y, x)
    return (r, theta)

# on import math une bibliotheque de mathematique par la suite on definie une fonction nommé 
# cartesien_vers_polaire qui a comme parametre la position x et y par la suite on crée une 
# variable nommé r donc rayon qui contient un parametre de la bibliotheque math avec 
# les parametre x et y puis une autre variable theta avec aussi un parametre de la 
# bibliotheque et les parameter y et x puis on return les deux variable

def extraire_points(lettre):
    points = []
    for ligne_idx, ligne in enumerate(lettre):
        for col_idx, led in enumerate(ligne):
            if led[0] == 1:
                x = col_idx
                y = ligne_idx
                r, theta = cartesien_vers_polaire(x, y)
                r_couleur = led[1]
                g_couleur = led[2]
                b_couleur = led[3]
                points.append((r, theta, r_couleur, g_couleur, b_couleur))
    return points

# une fonction nommé extraire_points avec le parametre lettre et je penses 
# que lettre sa sera je sais pas
# puis une variable points tableau 
# puis une boucle qui dit que pour l'index de la ligne et l ligne on enumerate (on numerote avec le parametre lettre) 
# puis une autre boucle pour la cologne qui donne index et cologne + on numerote et on parametre avec ligne donc sa sera coordonée
# puis on fais une conditions qui dit que si led == (egale) a 1 alors x variable index de la cologne + y variable index de la ligne
# puis on prend r et theta et on utilise la fonction cartesien vers polaire avec les parametre x et y 
# puis on assimile les couleurs rouge vert et bleau au led et ajoute les points avec les parametre suivants :
# r, theta, r_couleur, g_couleur, b_couleur
# par la suite on return les points
