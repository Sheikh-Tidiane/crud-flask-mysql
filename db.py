import mysql.connector
from mysql.connector import Error

# Configuration de la base de données
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'programmation',
    'database': 'flask_db',
}

def creer_connexion():
    """Établit une connexion à la base de données MySQL."""
    try:
        connexion = mysql.connector.connect(**DB_CONFIG)
        if connexion.is_connected():
            print("Connexion établie avec MySQL")
            return connexion
    except Error as e:
        print(f"Erreur de connexion à MySQL: {e}")
        return None

def fermer_connexion(connexion):
    """Ferme la connexion à la base de données."""
    if connexion and connexion.is_connected():
        connexion.close()
        print("Connexion fermée")

# ✅ Fonction attendue par requetes.py
def get_connection():
    """Alias pour compatibilité avec les autres modules."""
    return creer_connexion()
