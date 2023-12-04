# library_logic.py

import csv
import uuid  # Importer le module uuid

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
    
    def add_multiple(self, books_to_add):
        self.books.extend(books_to_add)
    
    def take_book_by_id(self, book_id):
        for book in self.books:
            if int(book.book_id) == int(book_id):
                if book.available_copies > 0:
                    book.available_copies -= 1
                    return True, f"Vous avez emprunté '{book.title}'"
                else:
                    return False, f"Plus de copies disponibles pour '{book.title}'"
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
                return True, f"Le livre '{book.title}' a été supprimé de la bibliothèque"
        return False, "Livre non trouvé"

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

    
    def generate_primary_key(self):
        unique_id = self.primary_key_counter
        self.primary_key_counter += 1  # Incrémenter le compteur pour chaque nouvel identifiant
        return unique_id
    
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

                self.add_multiple(books_to_add)
                return True  # Indiquer que l'importation s'est déroulée avec succès
        except Exception as e:
            print(f"Erreur lors de l'importation : {str(e)}")
            return False

    
    def open_add_book_dialog(self):
        dialog = AddBookDialog(self)
        dialog.set_library_app_reference(self)  # Définir la référence à l'instance de LibraryApp
        dialog.exec_()
