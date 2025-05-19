from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import requetes
from functools import wraps
from werkzeug.security import check_password_hash

main = Blueprint('main', __name__)

# Décorateur pour protéger les routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('main.login'))
        return f(*args, **kwargs)
    return decorated_function

@main.route('/')
@login_required
def index():
    mot_cle = request.args.get('mot_cle', '')
    id_etudiant = request.args.get('id_etudiant', '')
    date_debut = request.args.get('date_debut', '')
    date_fin = request.args.get('date_fin', '')

    id_converti = int(id_etudiant) if id_etudiant and id_etudiant.isdigit() else None

    if any([mot_cle, id_converti, (date_debut and date_fin)]):
        etudiants = requetes.rechercher_etudiants(
            mot_cle=mot_cle,
            id_etudiant=id_converti,
            date_debut=date_debut if date_debut else None,
            date_fin=date_fin if date_fin else None
        )
    else:
        etudiants = requetes.lister_etudiants()

    return render_template('liste.html',
        etudiants=etudiants,
        recherche={
            'mot_cle': mot_cle,
            'id_etudiant': id_etudiant,
            'date_debut': date_debut,
            'date_fin': date_fin
        }
    )

@main.route('/ajouter', methods=['GET', 'POST'])
@login_required
def ajouter():
    if request.method == 'POST':
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        email = request.form.get('email')
        note_str = request.form.get('note')

        if not all([nom, prenom, email]):
            flash('Tous les champs obligatoires doivent être remplis', 'danger')
            return render_template('ajouter.html')

        try:
            note = float(note_str) if note_str else None
        except ValueError:
            flash('La note doit être un nombre valide', 'danger')
            return render_template('ajouter.html')

        if requetes.ajouter_etudiant(nom, prenom, email, note):
            flash('Étudiant ajouté avec succès', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Erreur lors de l\'ajout de l\'étudiant', 'danger')

    return render_template('ajouter.html')

@main.route('/modifier/<int:etudiant_id>', methods=['GET', 'POST'])
@login_required
def modifier(etudiant_id):
    etudiant = requetes.obtenir_etudiant(etudiant_id)
    if not etudiant:
        flash('Étudiant non trouvé', 'danger')
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        email = request.form.get('email')
        note_str = request.form.get('note')

        if not all([nom, prenom, email]):
            flash('Tous les champs obligatoires doivent être remplis', 'danger')
            return render_template('modifier.html', etudiant=etudiant)

        try:
            note = float(note_str) if note_str else None
        except ValueError:
            flash('La note doit être un nombre valide', 'danger')
            return render_template('modifier.html', etudiant=etudiant)

        if requetes.modifier_etudiant(etudiant_id, nom, prenom, email, note):
            flash('Étudiant modifié avec succès', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Erreur lors de la modification de l\'étudiant', 'danger')

    return render_template('modifier.html', etudiant=etudiant)

@main.route('/supprimer/<int:etudiant_id>')
@login_required
def supprimer(etudiant_id):
    if requetes.supprimer_etudiant(etudiant_id):
        flash('Étudiant supprimé avec succès', 'success')
    else:
        flash('Erreur lors de la suppression de l\'étudiant', 'danger')

    return redirect(url_for('main.index'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = requetes.get_user_by_email(email)

        if user:
            if check_password_hash(user['password_hash'], password):
                session['user_id'] = user['id']
                session['username'] = user['username']
                return redirect(url_for('main.index'))
            else:
                error = "Mot de passe incorrect."
        else:
            error = "Email non trouvé."

    return render_template('login.html', error=error)

@main.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('main.login'))
