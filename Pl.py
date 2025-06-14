# Partie 1 : Entrée (Input)
# Saisir les dimensions du problème et les coefficients
# Nombre de variables de décision et de contraintes
n = int(input("Entrez le nombre de variables de décision : "))
m = int(input("Entrez le nombre de contraintes : "))

# Saisir la fonction objectif (maximisation ou minimisation)
print("Entrez les coefficients de la fonction objectif (séparés par des espaces) :")
z = list(map(float, input().split()))

# Saisir les contraintes
print("Entrez les coefficients des contraintes :")
a = []
b = []
types = []  # Type de contrainte (≤, ≥, =)
for i in range(m):
    print(f"Contrainte {i+1} :")
    print("Coefficients des variables (séparés par des espaces) :")
    a.append(list(map(float, input().split())))
    print("Type de contrainte (≤, ≥, =) :")
    types.append(input().strip())
    print("Valeur b :")
    b.append(float(input()))

# Partie 2 : Corps du code
# Générer le tableau initial du simplexe avec la méthode du Big-M
import numpy as np

# Ajouter les variables de surplus, d'excès et artificielles selon le type de contrainte
M = 1e6  # Grande valeur pour le Big-M
c_extended = z + [0] * m  # Ajouter des zéros pour les variables slack/excess
artificial_indices = []

for i in range(m):
    if types[i] == "<=":
        # Ajouter une variable slack
        slack = [0] * m
        slack[i] = 1
        a[i] += slack
        c_extended.append(0)
    elif types[i] == ">=":
        # Ajouter une variable d'excès et une variable artificielle
        excess = [0] * m
        excess[i] = -1
        a[i] += excess
        c_extended.append(0)

        artificial = [0] * m
        artificial[i] = 1
        a[i] += artificial
        c_extended.append(M)  # Coefficient M pour la variable artificielle
        artificial_indices.append(len(c_extended) - 1)
    elif types[i] == "=":
        # Ajouter une variable artificielle uniquement
        artificial = [0] * m
        artificial[i] = 1
        a[i] += artificial
        c_extended.append(M)  # Coefficient M pour la variable artificielle
        artificial_indices.append(len(c_extended) - 1)

# Convertir le tableau des contraintes en numpy array
A = np.array(a)
B = np.array(b)
C = np.array(c_extended)

# Créer le tableau initial du simplexe
simplex_tableau = np.hstack((A, B.reshape(-1, 1)))

# Partie 3 : Algorithme du Simplexe avec Big-M
# Fonction pour trouver la colonne pivot

def find_pivot_column(table, c):
    return np.argmin(c[:-1])

# Fonction pour trouver la ligne pivot

def find_pivot_row(table, pivot_col):
    rows = []
    for i in range(len(table)):
        if table[i, pivot_col] > 0:
            rows.append(table[i, -1] / table[i, pivot_col])
        else:
            rows.append(np.inf)
    return np.argmin(rows)

# Algorithme du simplexe
while True:
    # Identifier la colonne pivot
    pivot_col = find_pivot_column(simplex_tableau, C)
    if C[pivot_col] >= 0:
        # Solution optimale trouvée
        break

    # Identifier la ligne pivot
    pivot_row = find_pivot_row(simplex_tableau, pivot_col)
    if pivot_row == np.inf:
        print("Problème non borné")
        break

    # Diviser la ligne pivot par l'élément pivot
    pivot_value = simplex_tableau[pivot_row, pivot_col]
    simplex_tableau[pivot_row, :] /= pivot_value

    # Mettre à jour les autres lignes
    for i in range(len(simplex_tableau)):
        if i != pivot_row:
            simplex_tableau[i, :] -= simplex_tableau[i, pivot_col] * simplex_tableau[pivot_row, :]

    # Mettre à jour le vecteur des coûts
    C -= C[pivot_col] * simplex_tableau[pivot_row, :]

# Partie 4 : Affichage
print("Tableau final du simplexe :")
print(simplex_tableau)
print("Valeurs optimales des variables :")
print(simplex_tableau[:, -1])
