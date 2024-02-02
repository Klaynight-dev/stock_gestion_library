# library_logic.py

import csv
import uuid  # Importer le module uuid
from logs import *

class user:
    def __init__(self, user_id, username, name, email, empreint=0):
        self.user_id = user_id
        self.fname = username
        self.name = name
        self.mail = email
        self.take = empreint

class User_gestion:
    def __init__(self):
        self.users = []
        self.primary_key_counter = 1  # Compteur pour générer des identifiants uniques numériques

    def add(self, user):
        self.users.append(user)
        log_action(f"Ajout d'un utilisateur : ID={user.user_id}, Fname='{user.fname}', name='{user.name}, Email='{user.mail}', Empreint={user.take}", success=True)
    
    def add_multiple(self, users_to_add):
        self.users.extend(users_to_add)

        # Méthode pour mettre à jour les détails d'un utilisateur
    def update_user_details(self, user):
        for index, existing_user in enumerate(self.users):
            if existing_user.user_id == user.user_id:
                self.users[index] = user  # Mettre à jour les détails du utilisateur dans la liste
                log_action(f"Mise à jour des détails du utilisateur : ID={user.user_id}, Fname='{user.fname}', name='{user.name}, Email='{user.mail}', Empreint={user.take}", success=True)
                break  # Sortir de la boucle une fois le utilisateur mis à jour

    # Méthode pour afficher les utilisateurs en fonction de différents critères de recherche
    def display_users(self, query=None, by_isbn=False, by_author=False, by_title=False, by_copies=False, by_publisher=False):
        if query:
            filtered_users = []
            for user in self.users:
                if (by_isbn and query.lower() in user.isbn.lower()) or \
                   (by_author and query.lower() in user.author.lower()) or \
                   (by_title and query.lower() in user.title.lower()) or \
                   (by_copies and query.lower() in str(user.available_copies).lower()) or \
                   (by_publisher and query.lower() in user.publisher.lower()):  # Recherche par Publisher
                    filtered_users.append(user)
            return filtered_users
        else:
            return self.users

    # Méthode pour importer des utilisateurs à partir d'un fichier CSV
    def import_from_csv(self, file_path):
        try:
            with open(file_path, newline='', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                users_to_add = []
                max_user_id = max([user.user_id for user in self.users], default=0)

                for row in csv_reader:
                    max_user_id += 1  # Incrémenter l'ID pour le nouveau utilisateur
                    user = user(
                        max_user_id,
                        row['Title'],
                        row['Author'],
                        row['Publisher'],
                        row['ISBN'],
                        int(row['Total Copies']),
                        int(row['Total Copies'])  # Disponibilité initiale égale au nombre total de copies
                    )
                    users_to_add.append(user)
                    log_action(f"Ajout d'un utilisateur : ID={max_user_id}, Titre='{row['Title']}', Auteur='{row['Author']}', Publisher='{row['Publisher']}', ISBN='{row['ISBN']}', max_copies='{int(row['Total Copies'])}', copie_dispo='{int(row['Total Copies'])}'", success=True)

                self.add_multiple(users_to_add)
                # Enregistrement de l'action dans les logs
                log_action(f"Importation réussie à partir de {file_path}", success=True)
                return True  # Indiquer que l'importation s'est déroulée avec succès
        except Exception as e:
            log_action(f"Erreur lors de l'importation depuis {file_path}: {str(e)}", success=False)
            print(f"Erreur lors de l'importation : {str(e)}")
            return False

    # Méthode pour obtenir un utilisateur par son ID
    def get_user_by_id(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                return user
        log_action(f"Aucun utilisateur trouvé avec l'ID={user_id}", success=False)
        return None  # Si aucun utilisateur correspondant à l'ID n'est trouvé

