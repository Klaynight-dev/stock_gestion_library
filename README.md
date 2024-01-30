# Jobi - Système de Gestion de Bibliothèque

## Description
Jobi est une application Python développée avec le framework PyQt5, offrant une interface utilisateur conviviale pour la gestion des ressources de bibliothèque, y compris les livres, les utilisateurs, et les opérations d'emprunt/retour.

## Fonctionnalités
- Gestion des Livres :
  - Ajouter, éditer et supprimer des livres
  - Suivre les détails des livres tels que le titre, l'auteur, l'éditeur, l'ISBN, et le nombre d'exemplaires
  - Rechercher des livres selon divers critères

- Gestion des Utilisateurs :
  - Fonctionnalités de base pour gérer les utilisateurs (plus de fonctionnalités peuvent être ajoutées)

- Emprunt et Retour :
  - Emprunter des livres en saisissant l'ID du livre
  - Retourner des livres en saisissant l'ID du livre
  - Visualiser et gérer les livres empruntés

- Importation et Exportation :
  - Importer les données des livres à partir d'un fichier CSV
  - Exporter les données des livres vers un fichier CSV

- Journalisation :
  - Enregistrement des actions, des erreurs, et des événements importants pour référence

## Comment Utiliser
1. Cloner le dépôt : `git clone https://github.com/Klaynight-dev/stock_gestion_library.git`
2. Installer les dépendances : `pip install -r requirements.txt`
3. Exécuter l'application : `python main.py`

## Structure du Projet
- `main.py` : Point d'entrée principal de l'application
- `logs.py` : Fonctions de journalisation
- `library_logic.py` : Logique de gestion de la bibliothèque
- `dialog_logic.py` : Logique pour les boîtes de dialogue (par exemple, la boîte de dialogue d'ajout de livre)
- `content/css/style.css` : Feuille de style CSS pour la mise en forme de l'interface graphique
- `icon.png` : Icône de l'application
- `data/save/saved_books.csv` : Données de livres sauvegardées au format CSV

## Contributeurs
- [Klaynight-dev](https://github.com/Klaynight-dev) - Responsable du développement

## Contributions
Les contributions sont les bienvenues ! Pour des suggestions, des problèmes, ou des améliorations, veuillez ouvrir une issue ou une pull request.

## Licence
Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.
