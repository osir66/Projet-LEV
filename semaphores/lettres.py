# 1 = Allumé
# 0 = Eteint
# 1er nombre = status de la LED
# 3 suivants = couleur en RGB

C_OFF = (0, 0, 0, 0)
C_A = (1, 255, 0, 0) # rouge
C_B = (1, 0, 0, 255) # Bleu
C_C = (1, 0, 255, 0) # Vert
C_TRI = (1, 255, 255, 0) # jaune
C_CAR = (1, 255, 165, 0) # orange
C_RON = (1, 0, 255, 255) # Bleu Ciel / Turquoise
C_ETO = (1, 255, 20, 100) # Rose
C_COE = (1, 255, 20, 255) # violet

LETTRES = {
    'A': [
        [C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF],
        [C_OFF, C_OFF, C_OFF, C_OFF, C_A,   C_A,   C_OFF, C_OFF, C_OFF, C_OFF],
        [C_OFF, C_OFF, C_OFF, C_A,   C_OFF, C_OFF, C_A,   C_OFF, C_OFF, C_OFF],
        [C_OFF, C_OFF, C_A,   C_OFF, C_OFF, C_OFF, C_OFF, C_A,   C_OFF, C_OFF],
        [C_OFF, C_A,   C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_A,   C_OFF],
        [C_OFF, C_A,   C_A,   C_A,   C_A,   C_A,   C_A,   C_A,   C_A,   C_OFF],
        [C_OFF, C_A,   C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_A,   C_OFF],
        [C_OFF, C_A,   C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_A,   C_OFF],
        [C_OFF, C_A,   C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_A,   C_OFF],
        [C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF],
    ],
    'B': [
        [C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF],
        [C_OFF, C_OFF, C_B,   C_B,   C_B,   C_B,   C_B,   C_OFF, C_OFF, C_OFF],
        [C_OFF, C_OFF, C_B,   C_OFF, C_OFF, C_OFF, C_OFF, C_B,   C_OFF, C_OFF],
        [C_OFF, C_OFF, C_B,   C_OFF, C_OFF, C_OFF, C_OFF, C_B,   C_OFF, C_OFF],
        [C_OFF, C_OFF, C_B,   C_B,   C_B,   C_B,   C_B,   C_OFF, C_OFF, C_OFF],
        [C_OFF, C_OFF, C_B,   C_OFF, C_OFF, C_OFF, C_OFF, C_B,   C_OFF, C_OFF],
        [C_OFF, C_OFF, C_B,   C_OFF, C_OFF, C_OFF, C_OFF, C_B,   C_OFF, C_OFF],
        [C_OFF, C_OFF, C_B,   C_OFF, C_OFF, C_OFF, C_OFF, C_B,   C_OFF, C_OFF],
        [C_OFF, C_OFF, C_B,   C_B,   C_B,   C_B,   C_B,   C_OFF, C_OFF, C_OFF],
        [C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF],
    ],
    'C': [
        [C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF],
        [C_OFF, C_OFF, C_OFF, C_C,   C_C,   C_C,   C_C,   C_OFF, C_OFF, C_OFF],
        [C_OFF, C_OFF, C_C,   C_OFF, C_OFF, C_OFF, C_OFF, C_C,   C_OFF, C_OFF],
        [C_OFF, C_OFF, C_C,   C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF],
        [C_OFF, C_OFF, C_C,   C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF],
        [C_OFF, C_OFF, C_C,   C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF],
        [C_OFF, C_OFF, C_C,   C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF],
        [C_OFF, C_OFF, C_C,   C_OFF, C_OFF, C_OFF, C_OFF, C_C,   C_OFF, C_OFF],
        [C_OFF, C_OFF, C_OFF, C_C,   C_C,   C_C,   C_C,   C_OFF, C_OFF, C_OFF],
        [C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF],
    ],
    'TRIANGLE': [
        [C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF],
        [C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF],
        [C_OFF, C_OFF, C_OFF, C_OFF, C_TRI, C_TRI, C_OFF, C_OFF, C_OFF, C_OFF],
        [C_OFF, C_OFF, C_OFF, C_TRI, C_OFF, C_OFF, C_TRI, C_OFF, C_OFF, C_OFF],
        [C_OFF, C_OFF, C_TRI, C_OFF, C_OFF, C_OFF, C_OFF, C_TRI, C_OFF, C_OFF],
        [C_OFF, C_TRI, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_TRI, C_OFF],
        [C_TRI, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_TRI],
        [C_TRI, C_TRI, C_TRI, C_TRI, C_TRI, C_TRI, C_TRI, C_TRI, C_TRI, C_TRI],
        [C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF],
        [C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF],
    ],
    'CARRE': [
        [C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF],
        [C_OFF, C_CAR, C_CAR, C_CAR, C_CAR, C_CAR, C_CAR, C_CAR, C_CAR, C_OFF],
        [C_OFF, C_CAR, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_CAR, C_OFF],
        [C_OFF, C_CAR, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_CAR, C_OFF],
        [C_OFF, C_CAR, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_CAR, C_OFF],
        [C_OFF, C_CAR, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_CAR, C_OFF],
        [C_OFF, C_CAR, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_CAR, C_OFF],
        [C_OFF, C_CAR, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_CAR, C_OFF],
        [C_OFF, C_CAR, C_CAR, C_CAR, C_CAR, C_CAR, C_CAR, C_CAR, C_CAR, C_OFF],
        [C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF],
    ],
    'ROND': [
        [C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF],
        [C_OFF, C_OFF, C_OFF, C_RON, C_RON, C_RON, C_RON, C_OFF, C_OFF, C_OFF],
        [C_OFF, C_OFF, C_RON, C_OFF, C_OFF, C_OFF, C_OFF, C_RON, C_OFF, C_OFF],
        [C_OFF, C_RON, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_RON, C_OFF],
        [C_OFF, C_RON, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_RON, C_OFF],
        [C_OFF, C_RON, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_RON, C_OFF],
        [C_OFF, C_RON, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_RON, C_OFF],
        [C_OFF, C_OFF, C_RON, C_OFF, C_OFF, C_OFF, C_OFF, C_RON, C_OFF, C_OFF],
        [C_OFF, C_OFF, C_OFF, C_RON, C_RON, C_RON, C_RON, C_OFF, C_OFF, C_OFF],
        [C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF],
    ],
    'ETOILE': [
        [C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF],
        [C_OFF, C_OFF, C_OFF, C_OFF, C_ETO, C_ETO, C_OFF, C_OFF, C_OFF, C_OFF],
        [C_OFF, C_OFF, C_OFF, C_ETO, C_ETO, C_ETO, C_ETO, C_OFF, C_OFF, C_OFF],
        [C_ETO, C_ETO, C_ETO, C_ETO, C_ETO, C_ETO, C_ETO, C_ETO, C_ETO, C_ETO],
        [C_OFF, C_ETO, C_ETO, C_ETO, C_ETO, C_ETO, C_ETO, C_ETO, C_ETO, C_OFF],
        [C_OFF, C_OFF, C_ETO, C_ETO, C_ETO, C_ETO, C_ETO, C_ETO, C_OFF, C_OFF],
        [C_OFF, C_ETO, C_ETO, C_ETO, C_OFF, C_OFF, C_ETO, C_ETO, C_ETO, C_OFF],
        [C_ETO, C_ETO, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_ETO, C_ETO],
        [C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF],
        [C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF],
    ],
    'COEUR': [
        [C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF],
        [C_OFF, C_OFF, C_COE, C_COE, C_OFF, C_OFF, C_COE, C_COE, C_OFF, C_OFF],
        [C_OFF, C_COE, C_COE, C_COE, C_COE, C_COE, C_COE, C_COE, C_COE, C_OFF],
        [C_COE, C_COE, C_COE, C_COE, C_COE, C_COE, C_COE, C_COE, C_COE, C_COE],
        [C_COE, C_COE, C_COE, C_COE, C_COE, C_COE, C_COE, C_COE, C_COE, C_COE],
        [C_OFF, C_COE, C_COE, C_COE, C_COE, C_COE, C_COE, C_COE, C_COE, C_OFF],
        [C_OFF, C_OFF, C_COE, C_COE, C_COE, C_COE, C_COE, C_COE, C_OFF, C_OFF],
        [C_OFF, C_OFF, C_OFF, C_COE, C_COE, C_COE, C_COE, C_OFF, C_OFF, C_OFF],
        [C_OFF, C_OFF, C_OFF, C_OFF, C_COE, C_COE, C_OFF, C_OFF, C_OFF, C_OFF],
        [C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF, C_OFF],
    ],
}