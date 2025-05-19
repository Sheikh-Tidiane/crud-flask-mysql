from werkzeug.security import generate_password_hash
import requetes

username = "admin"
email = "admin123@gmail.com"
mot_de_passe = "admin123"

mot_de_passe_hash = generate_password_hash(mot_de_passe)

if requetes.ajouter_utilisateur(username, email, mot_de_passe_hash):
    print("Administrateur créé avec succès.")
else:
    print("Erreur lors de la création de l'administrateur.")
