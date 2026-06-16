import math

def interpoler_segment(x1, y1, x2, y2, nb_points=30):
    return [(x1 + (i/nb_points)*(x2-x1), y1 + (i/nb_points)*(y2-y1)) for i in range(nb_points)]

# 1. On crée les sommets d'une vraie étoile en X,Y
sommets = []
for i in range(10):
    angle_rad = math.radians(i * 36 - 90) 
    r = 100 if i % 2 == 0 else 40
    sommets.append((r * math.cos(angle_rad), r * math.sin(angle_rad)))

# 2. On relie les traits avec plein de points (toujours en X,Y pour faire des traits droits)
points_xy = []
for i in range(10):
    p1 = sommets[i]
    p2 = sommets[(i + 1) % 10]
    points_xy.extend(interpoler_segment(p1[0], p1[1], p2[0], p2[1], 30))

# 3. On convertit cette étoile parfaite au format POLAIRE pour ton hélice
with open("etoile_test_polaire.csv", "w") as f:
    f.write("Point;R;Angle;Stylo\n")
    for i, (x, y) in enumerate(points_xy):
        rayon = math.hypot(x, y)
        angle = (math.degrees(math.atan2(y, x)) + 360) % 360
        f.write(f"P{i+1};{round(rayon,2)};{round(angle,2)};1\n")

print("Fichier 'etoile_test_polaire.csv' généré avec succès !")