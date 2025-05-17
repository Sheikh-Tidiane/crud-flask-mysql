from flask import Blueprint, render_template, request, redirect, url_for, flash
import requetes

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Page d'accueil - Liste des étudiants avec recherche."""
    # Récupération des paramètres de recherche
    mot_cle = request.args.get('mot_cle', '')
    id_etudiant = request.args.get('id_etudiant', '')
    date_debut = request.args.get('date_debut', '')
    date_fin = request.args.get('date_fin', '')
    
    # Conversion des valeurs pour la recherche
    id_converti = int(id_etudiant) if id_etudiant and id_etudiant.isdigit() else None
    
    # Recherche des étudiants selon les critères
    if any([mot_cle, id_converti, (date_debut and date_fin)]):
        etudiants = requetes.rechercher_etudiants(
            mot_cle=mot_cle,
            id_etudiant=id_converti,
            date_debut=date_debut if date_debut else None,
            date_fin=date_fin if date_fin else None
        )
    else:
        etudiants = requetes.lister_etudiants()
    
    return render_template(
        'liste.html', 
        etudiants=etudiants,
        recherche={
            'mot_cle': mot_cle,
            'id_etudiant': id_etudiant,
            'date_debut': date_debut,
            'date_fin': date_fin
        }
    )

@main.route('/ajouter', methods=['GET', 'POST'])
def ajouter():
    """Ajouter un nouvel étudiant."""
    if request.method == 'POST':
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        email = request.form.get('email')
        note_str = request.form.get('note')
        
        # Validation de base
        if not all([nom, prenom, email]):
            flash('Tous les champs obligatoires doivent être remplis', 'danger')
            return render_template('ajouter.html')
        
        # Conversion de la note
        try:
            note = float(note_str) if note_str else None
        except ValueError:
            flash('La note doit être un nombre valide', 'danger')
            return render_template('ajouter.html')
        
        # Ajout de l'étudiant
        if requetes.ajouter_etudiant(nom, prenom, email, note):
            flash('Étudiant ajouté avec succès', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Erreur lors de l\'ajout de l\'étudiant', 'danger')
    
    return render_template('ajouter.html')

@main.route('/modifier/<int:etudiant_id>', methods=['GET', 'POST'])
def modifier(etudiant_id):
    """Modifier un étudiant existant."""
    etudiant = requetes.obtenir_etudiant(etudiant_id)
    
    if not etudiant:
        flash('Étudiant non trouvé', 'danger')
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        email = request.form.get('email')
        note_str = request.form.get('note')
        
        # Validation de base
        if not all([nom, prenom, email]):
            flash('Tous les champs obligatoires doivent être remplis', 'danger')
            return render_template('modifier.html', etudiant=etudiant)
        
        # Conversion de la note
        try:
            note = float(note_str) if note_str else None
        except ValueError:
            flash('La note doit être un nombre valide', 'danger')
            return render_template('modifier.html', etudiant=etudiant)
        
        # Modification de l'étudiant
        if requetes.modifier_etudiant(etudiant_id, nom, prenom, email, note):
            flash('Étudiant modifié avec succès', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Erreur lors de la modification de l\'étudiant', 'danger')
    
    return render_template('modifier.html', etudiant=etudiant)

@main.route('/supprimer/<int:etudiant_id>')
def supprimer(etudiant_id):
    """Supprimer un étudiant."""
    if requetes.supprimer_etudiant(etudiant_id):
        flash('Étudiant supprimé avec succès', 'success')
    else:
        flash('Erreur lors de la suppression de l\'étudiant', 'danger')
    
    return redirect(url_for('main.index'))