# user_logic.py

import csv
import uuid  # Importer le module uuid
from logs import *

class User:
    def __init__(self, user_id, username, name, email, empreint=0, address=""):
        self.user_id = user_id
        self.fname = username
        self.name = name
        self.mail = email
        self.take = empreint
        self.address = address

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
    def display_users(self, query=None, by_fname=False, by_name=False, by_mail=False, by_address=False, by_take=False):
        if query:
            filtered_users = []
            for user in self.users:
                if (by_fname and query.lower() in user.fname.lower()) or \
                   (by_name and query.lower() in user.name.lower()) or \
                   (by_mail and query.lower() in user.mail.lower()) or \
                   (by_address and query.lower() in user.address.lower()) or \
                   (by_take and query.lower() in str(user.take).lower()):
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
                    max_user_id += 1
                    user = User(
                        max_user_id,
                        row['Fname'],
                        row['Name'],
                        row['Email'],
                        row.get('Address', ''),  # Adjusted to reflect the new column order
                        int(row['Empreint'])
                    )
                    users_to_add.append(user)
                    log_action(f"Ajout d'un utilisateur : ID={max_user_id}, First Name='{row['Fname']}', Name='{row['Name']}', Email='{row['Email']}', Address='{row.get('Address', '')}', Nombre d'empreint='{int(row['Empreint'])}'", success=True)

                self.add_multiple(users_to_add)
                log_action(f"Importation réussie à partir de {file_path}", success=True)
                return True
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


