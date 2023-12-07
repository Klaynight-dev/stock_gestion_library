# Gestion de Bibliothèque

Ce projet est une application de gestion de bibliothèque réalisée en Python utilisant la bibliothèque Tkinter pour l'interface graphique.

## Fonctionnalités

- **Ajout de Livres** : Permet d'ajouter de nouveaux livres à la bibliothèque en spécifiant le titre, l'auteur, l'ISBN et le nombre de copies.
- **Recherche de Livres** : Permet de rechercher des livres par titre, auteur, ISBN ou nombre d'exemplaires disponibles.
- **Emprunt et Retour de Livres** : Permet aux utilisateurs d'emprunter et de retourner des livres. Les exemplaires disponibles sont automatiquement mis à jour.
- **Suppression de Livres** : Possibilité de supprimer des livres de la bibliothèque.
- **Importation/Exportation depuis/vers CSV** : Permet d'importer et d'exporter les données de la bibliothèque au format CSV.

## Comment Utiliser

1. Assurez-vous d'avoir Python installé sur votre système.
2. Installez les dépendances en exécutant `pip install -r requirements.txt`.
3. Exécutez le fichier `gui.py` pour lancer l'application.
4. Utilisez l'interface graphique pour ajouter, rechercher, emprunter, retourner ou supprimer des livres.

## Structure du Projet

- **`gui.py`** : Fichier principal de l'interface graphique de l'application.
- **`library_logic.py`** : Contient les classes `Library` et `Book` pour la logique de gestion de la bibliothèque.
- **`utils.py`** : Contient des fonctions utilitaires, comme l'exportation vers CSV.