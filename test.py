# Demande des entrées utilisateur
salaire_base = float(input("Entrez le salaire de base : "))
jours_travailles = int(input("Entrez le nombre de jours travaillés : "))
nombre_enfants = int(input("Entrez le nombre d’enfants : "))
prime_technicite = float(input("Entrez la prime de technicité : "))
prime_transport = float(input("Entrez la prime de transport : "))
prime_enfant = float(input("Entrez le montant de la prime par enfant : "))

# Calcul des valeurs
taux_travail = jours_travailles / 26
prime_enfants = prime_enfant * nombre_enfants
salaire_brut = (salaire_base + prime_technicite + prime_transport + prime_enfants) * taux_travail

# Calcul des taxes
impot = 0.02 * salaire_brut
cnss = 0.265 * salaire_brut

# Calcul du salaire net
salaire_net = salaire_brut - impot - cnss
# Affichage du résultat
print(f"Le salaire net est : {salaire_net:.2f} FCFA")
print(f"prime_enfants est : {prime_enfants}")
print(f"taux_travailt est : {taux_travail}")
print(f"salaire_brut est : {salaire_brut}")
print(f"L'impot  est : {impot}")
print(f"Le cnss est : {cnss}")