-- Création de la base de données
CREATE DATABASE IF NOT EXISTS flask_db;
USE flask_db;

-- Création de la table étudiant
CREATE TABLE IF NOT EXISTS etudiants (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    note FLOAT,
    date_ajout DATETIME DEFAULT CURRENT_TIMESTAMP
);

SELECT * FROM etudiants;