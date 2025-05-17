from mysql.connector import Error
from db import creer_connexion, fermer_connexion

def lister_etudiants():
    """Récupère tous les étudiants de la base de données."""
    connexion = creer_connexion()
    etudiants = []
    
    if connexion:
        try:
            cursor = connexion.cursor(dictionary=True)
            cursor.execute("SELECT * FROM etudiants ORDER BY nom, prenom")
            etudiants = cursor.fetchall()
            cursor.close()
        except Error as e:
            print(f"Erreur lors de la récupération des étudiants: {e}")
        finally:
            fermer_connexion(connexion)
    
    return etudiants

def obtenir_etudiant(etudiant_id):
    """Récupère un étudiant spécifique par son ID."""
    connexion = creer_connexion()
    etudiant = None
    
    if connexion:
        try:
            cursor = connexion.cursor(dictionary=True)
            query = "SELECT * FROM etudiants WHERE id = %s"
            cursor.execute(query, (etudiant_id,))
            etudiant = cursor.fetchone()
            cursor.close()
        except Error as e:
            print(f"Erreur lors de la récupération de l'étudiant: {e}")
        finally:
            fermer_connexion(connexion)
    
    return etudiant

def ajouter_etudiant(nom, prenom, email, note):
    """Ajoute un nouvel étudiant dans la base de données."""
    connexion = creer_connexion()
    resultat = False
    
    if connexion:
        try:
            cursor = connexion.cursor()
            query = """
            INSERT INTO etudiants (nom, prenom, email, note)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (nom, prenom, email, note))
            connexion.commit()
            resultat = True
            cursor.close()
        except Error as e:
            print(f"Erreur lors de l'ajout de l'étudiant: {e}")
        finally:
            fermer_connexion(connexion)
    
    return resultat

def modifier_etudiant(etudiant_id, nom, prenom, email, note):
    """Modifie les informations d'un étudiant existant."""
    connexion = creer_connexion()
    resultat = False
    
    if connexion:
        try:
            cursor = connexion.cursor()
            query = """
            UPDATE etudiants 
            SET nom = %s, prenom = %s, email = %s, note = %s
            WHERE id = %s
            """
            cursor.execute(query, (nom, prenom, email, note, etudiant_id))
            connexion.commit()
            resultat = True
            cursor.close()
        except Error as e:
            print(f"Erreur lors de la modification de l'étudiant: {e}")
        finally:
            fermer_connexion(connexion)
    
    return resultat

def supprimer_etudiant(etudiant_id):
    """Supprime un étudiant de la base de données."""
    connexion = creer_connexion()
    resultat = False
    
    if connexion:
        try:
            cursor = connexion.cursor()
            query = "DELETE FROM etudiants WHERE id = %s"
            cursor.execute(query, (etudiant_id,))
            connexion.commit()
            resultat = True
            cursor.close()
        except Error as e:
            print(f"Erreur lors de la suppression de l'étudiant: {e}")
        finally:
            fermer_connexion(connexion)
    
    return resultat

def rechercher_etudiants(mot_cle=None, id_etudiant=None, date_debut=None, date_fin=None):
    """Recherche des étudiants selon différents critères."""
    connexion = creer_connexion()
    etudiants = []
    
    if connexion:
        try:
            cursor = connexion.cursor(dictionary=True)
            
            # Construction de la requête dynamique
            conditions = []
            parametres = []
            
            if mot_cle:
                conditions.append("(nom LIKE %s OR prenom LIKE %s)")
                parametres.extend([f"%{mot_cle}%", f"%{mot_cle}%"])
            
            if id_etudiant:
                conditions.append("id = %s")
                parametres.append(id_etudiant)
            
            if date_debut and date_fin:
                conditions.append("date_ajout BETWEEN %s AND %s")
                parametres.extend([date_debut, date_fin])
            
            query = "SELECT * FROM etudiants"
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            query += " ORDER BY nom, prenom"
            
            cursor.execute(query, parametres)
            etudiants = cursor.fetchall()
            cursor.close()
        except Error as e:
            print(f"Erreur lors de la recherche des étudiants: {e}")
        finally:
            fermer_connexion(connexion)
    
    return etudiants