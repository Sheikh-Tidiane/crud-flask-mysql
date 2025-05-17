// JavaScript pour l'application de gestion des étudiants

document.addEventListener('DOMContentLoaded', function() {
    // Auto-fermeture des messages d'alerte après 5 secondes
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Validation du formulaire d'ajout/modification
    const formulaires = document.querySelectorAll('form');
    formulaires.forEach(form => {
        form.addEventListener('submit', function(event) {
            // Validation basique côté client
            const email = form.querySelector('input[name="email"]');
            if (email && !validateEmail(email.value)) {
                event.preventDefault();
                alert('Veuillez saisir une adresse email valide.');
                email.focus();
            }

            const note = form.querySelector('input[name="note"]');
            if (note && note.value !== '' && (parseFloat(note.value) < 0 || parseFloat(note.value) > 20)) {
                event.preventDefault();
                alert('La note doit être comprise entre 0 et 20.');
                note.focus();
            }
        });
    });

    // Gestion de la recherche - réinitialiser les dates si vides
    const formRecherche = document.querySelector('form[action="/"]');
    if (formRecherche) {
        formRecherche.addEventListener('submit', function() {
            const dateDebut = document.getElementById('date_debut');
            const dateFin = document.getElementById('date_fin');
            
            // Si une seule date est remplie, afficher un avertissement
            if ((dateDebut.value && !dateFin.value) || (!dateDebut.value && dateFin.value)) {
                alert('Veuillez renseigner les deux dates pour filtrer par période.');
                return false;
            }
        });
    }
});

// Fonction de validation d'email
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(String(email).toLowerCase());
}

// Fonction de formatage de note
function formaterNote(note) {
    if (note === null || note === undefined || note === '') {
        return '<span class="badge bg-secondary">Non évalué</span>';
    }
    
    note = parseFloat(note);
    const couleur = note >= 10 ? 'success' : 'danger';
    return `<span class="badge bg-${couleur}">${note}/20</span>`;
}