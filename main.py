import sys
import csv
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QWidget, QComboBox, QMessageBox, QFileDialog, QTreeWidget,
    QTreeWidgetItem, QTableWidgetItem, QHeaderView, QDialog)
from PyQt5.QtGui import (QPixmap, QIcon)
from library_logic import *

class AddBookDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ajouter un livre")
        self.resize(300, 100)

        self.layout = QVBoxLayout()

        self.entry_title = QLineEdit()
        self.entry_title.setPlaceholderText("Titre du livre")
        self.layout.addWidget(self.entry_title)

        self.entry_author = QLineEdit()
        self.entry_author.setPlaceholderText("Auteur")
        self.layout.addWidget(self.entry_author)

        self.entry_isbn = QLineEdit()
        self.entry_isbn.setPlaceholderText("ISBN")
        self.layout.addWidget(self.entry_isbn)

        self.entry_copies = QLineEdit()
        self.entry_copies.setPlaceholderText("Nombre d'exemplaires")
        self.layout.addWidget(self.entry_copies)

        buttons_layout = QHBoxLayout()

        self.btn_add = QPushButton("Ajouter")
        self.btn_add.clicked.connect(self.add_book_to_list(self.key))
        buttons_layout.addWidget(self.btn_add)

        self.btn_cancel = QPushButton("Annuler")
        self.btn_cancel.clicked.connect(self.close)
        buttons_layout.addWidget(self.btn_cancel)

        self.layout.addLayout(buttons_layout)
        self.setLayout(self.layout)
        
#         self.secondary_books_table = QTreeWidget()
#         self.secondary_books_table.setColumnCount(4)
#         self.secondary_books_table.setHeaderLabels(["Titre", "Auteur", "ISBN", "Exemplaires"])
#         self.layout.addWidget(self.secondary_books_table)
        
        
    def add_book_to_list(self, key):
        book_id = None
        title = self.entry_title.text()
        author = self.entry_author.text() 
        isbn = self.entry_isbn.text()
        copies = self.entry_copies.text()

        if title and author and isbn and copies:
            new_book = Book(int(book_id), title, author, isbn, int(copies))
            self.library_app.library.add(new_book)
            books = self.library_app.library.display_books()
            self.library_app.update_book_table(books)

            self.entry_title.clear()
            self.entry_author.clear()
            self.entry_isbn.clear()
            self.entry_copies.clear()

class LibraryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion de bibliothèque")
        self.setGeometry(100, 100, 800, 500)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        
        # Déterminer le chemin du répertoire actuel
        current_dir = os.path.dirname(os.path.realpath(__file__))

        # Définir l'icône de l'application dans la barre des tâches
        app_icon = QIcon(os.path.join(current_dir, 'logo.png'))  # Assurez-vous que 'icon.png' est dans le même répertoire que votre script
        self.setWindowIcon(app_icon)
        
        # Afficher le logo dans la bannière
        logo_label = QLabel(self)
        pixmap = QPixmap(os.path.join(current_dir, 'logo.png'))  # Assurez-vous que 'logo.png' est dans le même répertoire que votre script
        logo_label.setPixmap(pixmap)
        logo_label.setGeometry(10, 10, 200, 100)  # Définissez les dimensions et l'emplacement du logo
        
        self.library = Library()
        self.setup_search_section()
        self.setup_book_table()
        self.setup_borrow_return_remove_sections()
        self.setup_import_export_buttons()

    def open_add_book_dialog(self):
        dialog = AddBookDialog(self)
        dialog.library_app = self
        dialog.exec_()
        
    def setup_search_section(self):
        search_layout = QHBoxLayout()

        self.search_label = QLabel("Recherche:")
        self.entry_search = QLineEdit()
        self.entry_search.textChanged.connect(self.search_books)
        search_layout.addWidget(self.search_label)
        search_layout.addWidget(self.entry_search)

        self.search_type_label = QLabel("Type :")
        self.search_combobox = QComboBox()
        search_options = ["Titre", "Auteur", "ISBN", "Exemplaires"]#, "ID"]
        self.search_combobox.addItems(search_options)
        self.search_combobox.currentIndexChanged.connect(self.search_books)
        search_layout.addWidget(self.search_type_label)
        search_layout.addWidget(self.search_combobox)

        self.layout.addLayout(search_layout)

    def setup_book_table(self):
        self.book_table = QTreeWidget()
        self.book_table.setColumnCount(5)  # Ajouter une colonne pour l'ID unique
        self.book_table.setHeaderLabels(["ID", "Titre", "Auteur", "ISBN", "Exemplaires disponibles"])
        header = self.book_table.header()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.layout.addWidget(self.book_table)


    def setup_borrow_return_remove_sections(self):
        borrow_return_layout = QHBoxLayout()

        self.borrow_label = QLabel("ID à emprunter:")
        self.entry_take = QLineEdit()
        borrow_return_layout.addWidget(self.borrow_label)
        borrow_return_layout.addWidget(self.entry_take)

        self.btn_take = QPushButton("Emprunter")
        self.btn_take.clicked.connect(self.take_book)
        borrow_return_layout.addWidget(self.btn_take)

        self.return_label = QLabel("ID à retourner:")
        self.entry_return = QLineEdit()
        borrow_return_layout.addWidget(self.return_label)
        borrow_return_layout.addWidget(self.entry_return)

        self.btn_return = QPushButton("Retourner")
        self.btn_return.clicked.connect(self.return_book)
        borrow_return_layout.addWidget(self.btn_return)

        self.remove_label = QLabel("ID à supprimer:")
        self.entry_remove = QLineEdit()
        borrow_return_layout.addWidget(self.remove_label)
        borrow_return_layout.addWidget(self.entry_remove)

        self.btn_remove = QPushButton("Supprimer livre")
        self.btn_remove.clicked.connect(self.remove_book)
        borrow_return_layout.addWidget(self.btn_remove)

        self.layout.addLayout(borrow_return_layout)

    def setup_import_export_buttons(self):
        self.import_export_layout = QHBoxLayout()
        print("Setting up import/export buttons...")

        self.btn_import = QPushButton("Importer depuis CSV")
        self.btn_import.clicked.connect(self.import_from_csv)
        self.import_export_layout.addWidget(self.btn_import)

        self.btn_export = QPushButton("Exporter vers CSV")
        self.btn_export.clicked.connect(self.export_to_csv)
        self.import_export_layout.addWidget(self.btn_export)

        self.btn_open_add_book_dialog = QPushButton("Ajouter un livre")
        self.btn_open_add_book_dialog.clicked.connect(self.open_add_book_dialog)
        self.import_export_layout.addWidget(self.btn_open_add_book_dialog)

        self.layout.addLayout(self.import_export_layout)
        self.layout.update()
        print(self.import_export_layout.count())


    # Ajoute cette méthode dans AddBookDialog
    def set_library_app_reference(self, library_app):
        self.library_app = library_app


    def search_books(self):
        query = self.entry_search.text()
        search_type = self.search_combobox.currentText()

        if search_type == "ISBN":
            books = self.library.display_books(query=query, by_isbn=True)
        elif search_type == "Titre":
            books = self.library.display_books(query=query, by_title=True)
        elif search_type == "Auteur":
            books = self.library.display_books(query=query, by_author=True)
        elif search_type == "Exemplaires":
            books = self.library.display_books(query=query, by_copies=True)
        else:
            books = self.library.display_books(query=query)

        self.update_book_table(books)

    def update_book_table(self, books=None):
        self.book_table.clear()
        if not books:
            books = self.library.display_books()

        for book in books:
            item = QTreeWidgetItem(self.book_table)
            item.setText(0, str(book.book_id))
            item.setText(1, book.title)
            item.setText(2, book.author)
            item.setText(3, book.isbn)
            item.setText(4, str(book.available_copies))

    def take_book(self):
        book_id = self.entry_take.text()
        success, message = self.library.take_book_by_id(book_id)
        if success:
            QMessageBox.information(self, "Emprunt", message)
            self.update_book_table()
        else:
            QMessageBox.warning(self, "Emprunt impossible", message)

    def return_book(self):
        book_id = self.entry_return.text()
        success, message = self.library.return_book_by_id(book_id)
        if success:
            QMessageBox.information(self, "Retour", message)
            self.update_book_table()
        else:
            QMessageBox.warning(self, "Retour impossible", message)

    def remove_book(self):
        book_id = self.entry_remove.text()
        success, message = self.library.remove_book_by_id(book_id)
        if success:
            QMessageBox.information(self, "Suppression", message)
            self.update_book_table()
        else:
            QMessageBox.warning(self, "Suppression impossible", message)

    def import_from_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Sélectionner un fichier CSV", "", "CSV Files (*.csv)")
        if file_path:
            success = self.library.import_from_csv(file_path)
            if success:
                QMessageBox.information(self, "Importation réussie", "Les livres ont été importés avec succès depuis le fichier CSV.")
                self.update_book_table()
            else:
                QMessageBox.critical(self, "Erreur d'importation", "Une erreur est survenue lors de l'importation depuis le fichier CSV.")
                
    def export_to_csv(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Enregistrer le fichier CSV", "", "CSV Files (*.csv)")
        if file_path:
            try:
                with open(file_path, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Titre', 'Auteur', 'ISBN', 'Exemplaires disponibles'])
                    for book in self.library.display_books():
                        writer.writerow([book.title, book.author, book.isbn, book.available_copies])
                QMessageBox.information(self, "Exportation réussie", "Les données ont été exportées avec succès vers un fichier CSV.")
            except Exception as e:
                QMessageBox.critical(self, "Erreur d'exportation", f"Une erreur est survenue lors de l'exportation : {str(e)}")


def main():
    app = QApplication(sys.argv)
    
    # Définir les variables d'environnement pour gérer l'échelle des périphériques
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"  # Activer le facteur d'échelle par écran contrôlé par le plugin de la plateforme
    os.environ["QT_SCREEN_SCALE_FACTORS"] = "1"  # Définir les DPI spécifiques pour chaque écran
    os.environ["QT_SCALE_FACTOR"] = "1"  # Définir le facteur d'échelle global pour l'application
    
    window = LibraryApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()