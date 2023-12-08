# library_logic.py

import csv
import uuid  # Importer le module uuid
from logs import *

class Book:
    def __init__(self, book_id, title, author, publisher, isbn, total_copies, available_copies):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.total_copies = total_copies
        self.available_copies = available_copies
        self.publisher = publisher

class Library:
    def __init__(self):
        self.books = []
        self.primary_key_counter = 1  # Compteur pour générer des identifiants uniques numériques

    def add(self, book):
        self.books.append(book)
        log_action(f"Ajout d'un livre : ID={book.book_id}, Titre='{book.title}', Auteur='{book.author}', ISBN='{book.isbn}'", success=True)
    
    def add_multiple(self, books_to_add):
        self.books.extend(books_to_add)
    
    def take_book_by_id(self, book_id):
        for book in self.books:
            if int(book.book_id) == int(book_id):
                if book.available_copies > 0:
                    book.available_copies -= 1
                    log_action("Vous avez emprunté '{book.title}'")
                    return True, f"Vous avez emprunté '{book.title}'"
                else:
                    log_action(f"Plus de copies disponibles pour '{book.title}'")
                    return False, f"Plus de copies disponibles pour '{book.title}'"
        log_action("Livre non trouvé")
        return False, "Livre non trouvé"

    def return_book_by_id(self, book_id):
        for book in self.books:
            if int(book.book_id) == int(book_id):
                if book.available_copies < book.total_copies:
                    book.available_copies += 1
                    return True, f"Vous avez retourné '{book.title}'"
                else:
                    return False, f"Toutes les copies de '{book.title}' sont déjà retournées"
        return False, "Livre non trouvé"
    
    def remove_book_by_id(self, book_id):
        for book in self.books:
            if int(book.book_id) == int(book_id):
                self.books.remove(book)
                log_action(f"Suppression d'un livre : ID={book.book_id}, Titre='{book.title}', Auteur='{book.author}', ISBN='{book.isbn}'", success=True)
                return True, f"Le livre '{book.title}' a été supprimé de la bibliothèque"
        log_action(f"Tentative de suppression d'un livre avec l'ID='{book_id}'", success=False)
        return False, "Livre non trouvé"
    
        # Méthode pour mettre à jour les détails d'un livre
    def update_book_details(self, book):
        for index, existing_book in enumerate(self.books):
            if existing_book.book_id == book.book_id:
                self.books[index] = book  # Mettre à jour les détails du livre dans la liste
                log_action(f"Mise à jour des détails du livre : ID={book.book_id}, Titre='{book.title}', Auteur='{book.author}', ISBN='{book.isbn}'", success=True)
                break  # Sortir de la boucle une fois le livre mis à jour

    # Méthode pour afficher les livres en fonction de différents critères de recherche
    def display_books(self, query=None, by_isbn=False, by_author=False, by_title=False, by_copies=False, by_publisher=False):
        if query:
            filtered_books = []
            for book in self.books:
                if (by_isbn and query.lower() in book.isbn.lower()) or \
                   (by_author and query.lower() in book.author.lower()) or \
                   (by_title and query.lower() in book.title.lower()) or \
                   (by_copies and query.lower() in str(book.available_copies).lower()) or \
                   (by_publisher and query.lower() in book.publisher.lower()):  # Recherche par Publisher
                    filtered_books.append(book)
            return filtered_books
        else:
            return self.books

    # Méthode pour importer des livres à partir d'un fichier CSV
    def import_from_csv(self, file_path):
        try:
            with open(file_path, newline='', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                books_to_add = []
                max_book_id = max([book.book_id for book in self.books], default=0)

                for row in csv_reader:
                    max_book_id += 1  # Incrémenter l'ID pour le nouveau livre
                    book = Book(
                        max_book_id,
                        row['Title'],
                        row['Author'],
                        row['Publisher'],
                        row['ISBN'],
                        int(row['Total Copies']),
                        int(row['Total Copies'])  # Disponibilité initiale égale au nombre total de copies
                    )
                    books_to_add.append(book)
                    log_action(f"Ajout d'un livre : ID={max_book_id}, Titre='{row['Title']}', Auteur='{row['Author']}', Publisher='{row['Publisher']}', ISBN='{row['ISBN']}', max_copies='{int(row['Total Copies'])}', copie_dispo='{int(row['Total Copies'])}'", success=True)

                self.add_multiple(books_to_add)
                # Enregistrement de l'action dans les logs
                log_action(f"Importation réussie à partir de {file_path}", success=True)
                return True  # Indiquer que l'importation s'est déroulée avec succès
        except Exception as e:
            log_action(f"Erreur lors de l'importation depuis {file_path}: {str(e)}", success=False)
            print(f"Erreur lors de l'importation : {str(e)}")
            return False

    # Méthode pour obtenir un livre par son ID
    def get_book_by_id(self, book_id):
        for book in self.books:
            if book.book_id == book_id:
                return book
        log_action(f"Aucun livre trouvé avec l'ID={book_id}", success=False)
        return None  # Si aucun livre correspondant à l'ID n'est trouvé
